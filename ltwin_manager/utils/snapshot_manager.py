# -*- coding: utf-8 -*-
"""
快照管理器
用于管理虚拟机快照的创建、恢复、删除等操作
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import shutil


class Snapshot:
    """快照数据类"""
    def __init__(self, vm_name: str, snapshot_id: str, name: str, description: str = "", 
                 created_at: str = None, parent_id: str = None):
        self.vm_name = vm_name
        self.id = snapshot_id
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.parent_id = parent_id  # 父快照ID，用于构建快照链


class SnapshotManager:
    """快照管理器"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        snapshot_location = self.config_manager.get_global_config("snapshot_location")
        if snapshot_location is None:
            # 如果没有配置快照位置，则使用默认位置
            snapshot_location = os.path.join(os.path.expanduser('~'), '.ltwin', 'snapshots')
        self.snapshots_dir = Path(snapshot_location)
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        
        # 快照元数据文件
        self.metadata_file = self.snapshots_dir / "snapshots.json"
        self.snapshots_metadata = self._load_snapshots_metadata()
    
    def _load_snapshots_metadata(self) -> Dict:
        """加载快照元数据"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载快照元数据失败: {e}")
                return {}
        return {}
    
    def _save_snapshots_metadata(self):
        """保存快照元数据"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.snapshots_metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存快照元数据失败: {e}")
    
    def create_snapshot(self, vm_name: str, snapshot_name: str, description: str = "") -> bool:
        """创建虚拟机快照"""
        try:
            # 获取虚拟机配置
            vm_config = self.config_manager.get_vm_config(vm_name)
            if not vm_config:
                raise ValueError(f"虚拟机 '{vm_name}' 不存在")
            
            # 确保虚拟机正在运行
            if vm_config.get('status') != 'running':
                raise ValueError(f"虚拟机 '{vm_name}' 未运行，无法创建快照")
            
            # 生成快照ID
            snapshot_id = f"{vm_name}_snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # 创建快照目录
            snapshot_dir = self.snapshots_dir / vm_name / snapshot_id
            snapshot_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建快照 - 对于qcow2格式，我们可以使用qemu-img
            disk_path = vm_config['disk_path']
            snapshot_path = snapshot_dir / f"{vm_name}_snapshot.qcow2"
            
            # 使用qemu-img创建快照
            cmd = [
                'qemu-img', 'create',
                '-f', 'qcow2',
                '-b', disk_path,  # 基础镜像
                '-F', 'qcow2',    # 基础镜像格式
                str(snapshot_path)
            ]
            
            subprocess.run(cmd, check=True)
            
            # 保存快照元数据
            if vm_name not in self.snapshots_metadata:
                self.snapshots_metadata[vm_name] = {}
                
            self.snapshots_metadata[vm_name][snapshot_id] = {
                'id': snapshot_id,
                'name': snapshot_name,
                'description': description,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'disk_path': str(snapshot_path),
                'vm_state': 'stopped'  # 记录虚拟机状态
            }
            
            self._save_snapshots_metadata()
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"创建快照失败: {e}")
            return False
        except Exception as e:
            print(f"创建快照时发生错误: {e}")
            return False
    
    def restore_snapshot(self, vm_name: str, snapshot_id: str) -> bool:
        """恢复虚拟机快照"""
        try:
            # 检查快照是否存在
            if vm_name not in self.snapshots_metadata or snapshot_id not in self.snapshots_metadata[vm_name]:
                raise ValueError(f"快照 '{snapshot_id}' 不存在")
            
            # 获取虚拟机配置
            vm_config = self.config_manager.get_vm_config(vm_name)
            if not vm_config:
                raise ValueError(f"虚拟机 '{vm_name}' 不存在")
            
            # 确保虚拟机已停止
            if vm_config.get('status') == 'running':
                raise ValueError(f"请先停止虚拟机 '{vm_name}' 再恢复快照")
            
            # 获取快照信息
            snapshot_info = self.snapshots_metadata[vm_name][snapshot_id]
            snapshot_path = snapshot_info['disk_path']
            
            # 使用qemu-img将快照合并回原始磁盘
            original_disk_path = vm_config['disk_path']
            
            # 首先备份原磁盘
            backup_path = f"{original_disk_path}.backup"
            shutil.copy2(original_disk_path, backup_path)
            
            # 将快照内容复制回原磁盘
            cmd = [
                'qemu-img', 'convert',
                '-f', 'qcow2',
                '-O', 'qcow2',
                snapshot_path,
                original_disk_path
            ]
            
            subprocess.run(cmd, check=True)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"恢复快照失败: {e}")
            return False
        except Exception as e:
            print(f"恢复快照时发生错误: {e}")
            return False
    
    def delete_snapshot(self, vm_name: str, snapshot_id: str) -> bool:
        """删除虚拟机快照"""
        try:
            # 检查快照是否存在
            if vm_name not in self.snapshots_metadata or snapshot_id not in self.snapshots_metadata[vm_name]:
                raise ValueError(f"快照 '{snapshot_id}' 不存在")
            
            # 删除快照文件
            snapshot_info = self.snapshots_metadata[vm_name][snapshot_id]
            snapshot_path = Path(snapshot_info['disk_path'])
            
            if snapshot_path.exists():
                snapshot_path.unlink()
            
            # 删除快照目录
            snapshot_dir = snapshot_path.parent
            if snapshot_dir.exists() and len(list(snapshot_dir.iterdir())) == 0:
                snapshot_dir.rmdir()
            
            # 从元数据中移除
            del self.snapshots_metadata[vm_name][snapshot_id]
            
            # 如果该虚拟机没有其他快照，则删除虚拟机条目
            if not self.snapshots_metadata[vm_name]:
                del self.snapshots_metadata[vm_name]
            
            self._save_snapshots_metadata()
            return True
            
        except Exception as e:
            print(f"删除快照失败: {e}")
            return False
    
    def list_snapshots(self, vm_name: str) -> List[Dict]:
        """列出虚拟机的所有快照"""
        if vm_name not in self.snapshots_metadata:
            return []
        
        snapshots = []
        for snap_id, snap_info in self.snapshots_metadata[vm_name].items():
            snapshots.append({
                'id': snap_info['id'],
                'name': snap_info['name'],
                'description': snap_info['description'],
                'created_at': snap_info['created_at'],
                'vm_state': snap_info.get('vm_state', 'unknown')
            })
        
        # 按创建时间排序（最新的在前）
        snapshots.sort(key=lambda x: x['created_at'], reverse=True)
        return snapshots
    
    def get_snapshot_info(self, vm_name: str, snapshot_id: str) -> Optional[Dict]:
        """获取快照详细信息"""
        if vm_name in self.snapshots_metadata and snapshot_id in self.snapshots_metadata[vm_name]:
            return self.snapshots_metadata[vm_name][snapshot_id]
        return None


# 全局快照管理器实例
snapshot_manager = None


def get_snapshot_manager(config_manager) -> SnapshotManager:
    """获取快照管理器实例"""
    global snapshot_manager
    if snapshot_manager is None:
        snapshot_manager = SnapshotManager(config_manager)
    return snapshot_manager