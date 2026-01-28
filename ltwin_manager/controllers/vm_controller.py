# -*- coding: utf-8 -*-
"""
虚拟机控制器
负责虚拟机的创建、启动、停止等操作
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import psutil
import threading
import time


@dataclass
class VMConfig:
    name: str
    cpu_cores: int
    memory_mb: int
    disk_path: str
    iso_path: Optional[str] = None
    vnc_port: int = 5900
    network_mode: str = "用户模式 (User/NAT)"  # 更新为中文模式名
    mac_address: str = ""
    status: str = "stopped"
    created_at: str = ""
    last_started: str = ""


from ltwin_manager.utils.snapshot_manager import get_snapshot_manager
from ltwin_manager.utils.network_manager import get_network_manager
from ltwin_manager.utils.performance_optimizer import get_performance_optimizer

class VMController:
    def __init__(self, config_manager=None):
        self.vms: Dict[str, VMConfig] = {}
        self.running_processes: Dict[str, subprocess.Popen] = {}
        self.config_file = Path.home() / '.ltwin' / 'vms.json'
        self.config_manager = config_manager
        self.snapshot_manager = None
        if config_manager:
            self.snapshot_manager = get_snapshot_manager(config_manager)
        self.network_manager = get_network_manager()
        self.performance_optimizer = get_performance_optimizer()
        self.load_configs()
    
    def load_configs(self):
        """从配置文件加载虚拟机配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    configs = json.load(f)
                    for name, config_data in configs.items():
                        # 创建配置对象时只使用已知字段
                        vm_config = VMConfig(
                            name=config_data.get('name', ''),
                            cpu_cores=config_data.get('cpu_cores', 2),
                            memory_mb=config_data.get('memory_mb', 2048),
                            disk_path=config_data.get('disk_path', ''),
                            iso_path=config_data.get('iso_path'),
                            vnc_port=config_data.get('vnc_port', 5900),
                            network_mode=config_data.get('network_mode', '用户模式 (User/NAT)'),
                            mac_address=config_data.get('mac_address', ''),
                            status=config_data.get('status', 'stopped'),
                            created_at=config_data.get('created_at', ''),
                            last_started=config_data.get('last_started', '')
                        )
                        self.vms[name] = vm_config
            except Exception as e:
                print(f"加载配置文件失败: {e}")
    
    def save_configs(self):
        """保存虚拟机配置到文件"""
        config_dir = self.config_file.parent
        config_dir.mkdir(exist_ok=True)
        
        configs = {}
        for name, config in self.vms.items():
            configs[name] = {
                'name': config.name,
                'cpu_cores': config.cpu_cores,
                'memory_mb': config.memory_mb,
                'disk_path': config.disk_path,
                'iso_path': config.iso_path,
                'vnc_port': config.vnc_port,
                'network_mode': config.network_mode,
                'mac_address': config.mac_address,
                'status': config.status,
                'created_at': config.created_at,
                'last_started': config.last_started
            }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(configs, f, ensure_ascii=False, indent=2)
    
    def create_vm(self, config: VMConfig) -> bool:
        """创建新的虚拟机"""
        try:
            # 验证配置
            if not self.validate_config(config):
                return False
            
            # 创建虚拟磁盘（如果不存在）
            if not os.path.exists(config.disk_path):
                self.create_disk_image(config.disk_path, size_gb=20)
            
            # 保存配置
            self.vms[config.name] = config
            self.save_configs()
            
            return True
        except Exception as e:
            print(f"创建虚拟机失败: {e}")
            return False
    
    def validate_config(self, config: VMConfig) -> bool:
        """验证虚拟机配置"""
        # 检查名称是否重复
        if config.name in self.vms:
            raise ValueError(f"虚拟机名称 '{config.name}' 已存在")
        
        # 检查资源是否充足
        available_memory = psutil.virtual_memory().available
        if config.memory_mb * 1024 * 1024 > available_memory:
            raise ValueError("内存不足")
        
        # 检查磁盘空间
        disk_usage = psutil.disk_usage(os.path.dirname(config.disk_path))
        if 20 * 1024 * 1024 * 1024 > disk_usage.free:  # 假设最小20GB
            raise ValueError("磁盘空间不足")
        
        return True
    
    def create_disk_image(self, path: str, size_gb: int):
        """创建虚拟磁盘镜像"""
        cmd = [
            'qemu-img', 'create',
            '-f', 'qcow2',
            path,
            f'{size_gb}G'
        ]
        subprocess.run(cmd, check=True)
    
    def start_vm_with_config(self, config: dict) -> bool:
        """使用配置字典启动虚拟机"""
        # 构建QEMU命令
        cmd = [
            'qemu-system-x86_64',
            '-machine', 'q35',
            '-cpu', 'host',
        ]
        
        # 使用性能优化器优化命令
        config_with_name = config.copy() if isinstance(config, dict) else {**config}
        if 'name' not in config_with_name:
            config_with_name['name'] = config_with_name.get('name', 'unnamed')
        cmd = self.performance_optimizer.optimize_qemu_command(cmd, config_with_name)
        
        # 添加ISO镜像（如果有）
        iso_path = config.get('iso_path')
        if iso_path and os.path.exists(iso_path):
            cmd.extend(['-cdrom', iso_path])
        
        # 添加网络配置
        network_params = self.network_manager.configure_vm_network(
            config.get('name', ''),
            config.get('network_mode', '用户模式 (User/NAT)'),
            '',  # 桥接接口（暂不支持）
            config.get('mac_address', '')
        )
        cmd.extend(network_params)
        
        # 添加显示配置
        cmd.extend([
            '-vga', 'virtio',
            '-usb', '-device', 'usb-tablet',
            f'-vnc', f':{config.get("vnc_port", 5900) - 5900}'
        ])
        
        try:
            # 启动QEMU进程
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.running_processes[config.get('name')] = process
            config['status'] = "running"
            
            return True
        except Exception as e:
            print(f"启动虚拟机失败: {e}")
            config['status'] = "stopped"
            return False
    
    def start_vm(self, name: str) -> bool:
        """启动虚拟机"""
        if name not in self.vms:
            raise ValueError(f"虚拟机 '{name}' 不存在")
        
        config = self.vms[name]
        
        # 构建QEMU命令
        cmd = [
            'qemu-system-x86_64',
            '-machine', 'q35',
            '-cpu', 'host',
        ]
        
        # 使用性能优化器优化命令
        temp_config = {
            'cpu_cores': config.cpu_cores,
            'memory_mb': config.memory_mb,
            'disk_path': config.disk_path,
            'vnc_port': config.vnc_port,
            'name': config.name
        }
        cmd = self.performance_optimizer.optimize_qemu_command(cmd, temp_config)
        
        # 添加ISO镜像（如果有）
        if config.iso_path and os.path.exists(config.iso_path):
            cmd.extend(['-cdrom', config.iso_path])
        
        # 添加网络配置
        network_params = self.network_manager.configure_vm_network(
            config.name,
            config.network_mode,
            '',  # 桥接接口（暂不支持）
            config.mac_address
        )
        cmd.extend(network_params)
        
        # 添加显示配置
        cmd.extend([
            '-vga', 'virtio',
            '-usb', '-device', 'usb-tablet',
            f'-vnc', f':{config.vnc_port - 5900}'
        ])
        
        try:
            # 启动QEMU进程
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.running_processes[name] = process
            config.status = "running"
            self.save_configs()
            
            return True
        except Exception as e:
            print(f"启动虚拟机失败: {e}")
            config.status = "stopped"
            return False
    
    def stop_vm(self, name: str) -> bool:
        """停止虚拟机"""
        if name not in self.running_processes:
            print(f"虚拟机 '{name}' 未运行")
            return False
        
        process = self.running_processes[name]
        try:
            # 尝试优雅关闭
            process.terminate()
            try:
                process.wait(timeout=10)  # 等待10秒
            except subprocess.TimeoutExpired:
                # 强制终止
                process.kill()
                process.wait()
            
            del self.running_processes[name]
            
            # 更新状态
            if name in self.vms:
                self.vms[name].status = "stopped"
                self.save_configs()
            
            return True
        except Exception as e:
            print(f"停止虚拟机失败: {e}")
            return False
    
    def list_vms(self) -> List[Dict]:
        """列出所有虚拟机"""
        vms_list = []
        for name, config in self.vms.items():
            # 检查进程是否仍在运行
            if name in self.running_processes:
                process = self.running_processes[name]
                if process.poll() is not None:  # 进程已结束
                    del self.running_processes[name]
                    config.status = "stopped"
                    self.save_configs()
            
            vms_list.append({
                'name': config.name,
                'cpu_cores': config.cpu_cores,
                'memory_mb': config.memory_mb,
                'disk_path': config.disk_path,
                'iso_path': config.iso_path,
                'vnc_port': config.vnc_port,
                'network_mode': config.network_mode,
                'mac_address': config.mac_address,
                'status': config.status,
                'created_at': config.created_at,
                'last_started': config.last_started
            })
        
        return vms_list
    
    def get_vm_status(self, name: str) -> Optional[Dict]:
        """获取虚拟机状态"""
        if name not in self.vms:
            return None
        
        config = self.vms[name]
        is_running = name in self.running_processes and self.running_processes[name].poll() is None
        
        return {
            'name': config.name,
            'status': 'running' if is_running else config.status,
            'cpu_cores': config.cpu_cores,
            'memory_mb': config.memory_mb,
            'disk_path': config.disk_path
        }
    
    def create_vm_snapshot(self, vm_name: str, snapshot_name: str, description: str = "") -> bool:
        """创建虚拟机快照"""
        if not self.snapshot_manager:
            print("快照功能未启用")
            return False
        
        return self.snapshot_manager.create_snapshot(vm_name, snapshot_name, description)
    
    def restore_vm_snapshot(self, vm_name: str, snapshot_id: str) -> bool:
        """恢复虚拟机快照"""
        if not self.snapshot_manager:
            print("快照功能未启用")
            return False
        
        return self.snapshot_manager.restore_snapshot(vm_name, snapshot_id)
    
    def delete_vm_snapshot(self, vm_name: str, snapshot_id: str) -> bool:
        """删除虚拟机快照"""
        if not self.snapshot_manager:
            print("快照功能未启用")
            return False
        
        return self.snapshot_manager.delete_snapshot(vm_name, snapshot_id)
    
    def list_vm_snapshots(self, vm_name: str) -> List[Dict]:
        """列出虚拟机快照"""
        if not self.snapshot_manager:
            print("快照功能未启用")
            return []
        
        return self.snapshot_manager.list_snapshots(vm_name)
    
    def get_vm_snapshots_info(self, vm_name: str, snapshot_id: str) -> Optional[Dict]:
        """获取快照详细信息"""
        if not self.snapshot_manager:
            print("快照功能未启用")
            return None
        
        return self.snapshot_manager.get_snapshot_info(vm_name, snapshot_id)