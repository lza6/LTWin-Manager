# -*- coding: utf-8 -*-
"""
克隆管理器
用于管理虚拟机克隆操作
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class CloneManager:
    """克隆管理器"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
    
    def clone_vm(self, source_vm_name: str, target_vm_name: str, clone_type: str = "full", 
                 target_disk_path: str = None) -> bool:
        """
        克隆虚拟机
        
        Args:
            source_vm_name: 源虚拟机名称
            target_vm_name: 目标虚拟机名称
            clone_type: 克隆类型 - "full"(完全克隆) 或 "linked"(链接克隆)
            target_disk_path: 目标磁盘路径（如果不指定则自动生成）
        
        Returns:
            bool: 是否克隆成功
        """
        try:
            # 获取源虚拟机配置
            source_config = self.config_manager.get_vm_config(source_vm_name)
            if not source_config:
                raise ValueError(f"源虚拟机 '{source_vm_name}' 不存在")
            
            # 检查目标虚拟机是否已存在
            if self.config_manager.vm_exists(target_vm_name):
                raise ValueError(f"目标虚拟机 '{target_vm_name}' 已存在")
            
            # 确定目标磁盘路径
            if not target_disk_path:
                vm_storage_path = self.config_manager.get_default_vm_storage_path()
                target_disk_path = str(vm_storage_path / f"{target_vm_name}.qcow2")
            
            # 根据克隆类型执行相应操作
            if clone_type == "full":
                # 完全克隆 - 复制整个磁盘文件
                source_disk_path = source_config['disk_path']
                self._full_clone(source_disk_path, target_disk_path)
            elif clone_type == "linked":
                # 链接克隆 - 基于源磁盘创建差异磁盘
                source_disk_path = source_config['disk_path']
                self._linked_clone(source_disk_path, target_disk_path)
            else:
                raise ValueError(f"不支持的克隆类型: {clone_type}")
            
            # 创建新的虚拟机配置
            new_config = source_config.copy()
            new_config['name'] = target_vm_name
            new_config['disk_path'] = target_disk_path
            new_config['status'] = 'stopped'
            new_config['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 生成新的MAC地址（如果原配置中有MAC地址）
            if new_config.get('mac_address'):
                new_config['mac_address'] = self._generate_new_mac()
            
            # 生成新的VNC端口
            new_config['vnc_port'] = self.config_manager.get_next_vnc_port()
            
            # 保存新虚拟机配置
            self.config_manager.set_vm_config(target_vm_name, new_config)
            
            return True
            
        except Exception as e:
            print(f"克隆虚拟机失败: {e}")
            return False
    
    def _full_clone(self, source_disk: str, target_disk: str):
        """执行完全克隆"""
        # 确保目标目录存在
        target_path = Path(target_disk)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 使用qemu-img进行磁盘克隆
        cmd = [
            'qemu-img', 'convert',
            '-f', 'qcow2',
            '-O', 'qcow2',
            source_disk,
            target_disk
        ]
        
        subprocess.run(cmd, check=True)
    
    def _linked_clone(self, source_disk: str, target_disk: str):
        """执行链接克隆"""
        # 确保目标目录存在
        target_path = Path(target_disk)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建基于源磁盘的链接克隆
        cmd = [
            'qemu-img', 'create',
            '-f', 'qcow2',
            '-b', source_disk,  # 基础镜像
            '-F', 'qcow2',     # 基础镜像格式
            target_disk
        ]
        
        subprocess.run(cmd, check=True)
    
    def _generate_new_mac(self) -> str:
        """生成新的MAC地址"""
        import random
        # 生成随机MAC地址（以52:54:00开头，这是QEMU默认的OUI）
        mac = [0x52, 0x54, 0x00,
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0xff),
               random.randint(0x00, 0xff)]
        return ':'.join(map(lambda x: "%02x" % x, mac))


# 全局克隆管理器实例
clone_manager = None


def get_clone_manager(config_manager) -> CloneManager:
    """获取克隆管理器实例"""
    global clone_manager
    if clone_manager is None:
        clone_manager = CloneManager(config_manager)
    return clone_manager