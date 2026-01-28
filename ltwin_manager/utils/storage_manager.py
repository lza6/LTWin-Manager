# -*- coding: utf-8 -*-
"""
存储管理器
用于管理虚拟机磁盘存储、快照存储等功能
"""

import os
import shutil
import psutil
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
import subprocess


@dataclass
class DiskInfo:
    """磁盘信息数据类"""
    name: str
    path: str
    total_size: int
    used_size: int
    free_size: int
    usage_percent: float


@dataclass
class FileInfo:
    """文件信息数据类"""
    name: str
    path: str
    size: int
    is_directory: bool
    modified_time: float


class StorageManager:
    """存储管理器"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        vm_storage_path = config_manager.get_global_config("vm_storage_path")
        self.base_path = Path(vm_storage_path) if vm_storage_path else Path.home() / "VirtualMachines"
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def get_system_disks(self) -> List[DiskInfo]:
        """获取系统磁盘信息"""
        disks = []
        
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info = DiskInfo(
                    name=partition.device,
                    path=partition.mountpoint,
                    total_size=usage.total,
                    used_size=usage.used,
                    free_size=usage.free,
                    usage_percent=(usage.used / usage.total) * 100 if usage.total > 0 else 0
                )
                disks.append(disk_info)
            except PermissionError:
                continue
        
        return disks
    
    def get_ltwin_storage_usage(self) -> DiskInfo:
        """获取LTWin存储使用情况"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(self.base_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except OSError:
                    continue  # 忽略无法访问的文件
        
        # 获取所在磁盘的总信息
        disk_usage = psutil.disk_usage(str(self.base_path))
        
        return DiskInfo(
            name="LTWin存储",
            path=str(self.base_path),
            total_size=disk_usage.total,
            used_size=total_size,
            free_size=disk_usage.free,
            usage_percent=(total_size / disk_usage.total) * 100 if disk_usage.total > 0 else 0
        )
    
    def list_directory(self, path: str) -> List[FileInfo]:
        """列出目录内容"""
        path_obj = Path(path)
        if not path_obj.exists() or not path_obj.is_dir():
            return []
        
        files = []
        for item in path_obj.iterdir():
            try:
                stat = item.stat()
                file_info = FileInfo(
                    name=item.name,
                    path=str(item),
                    size=stat.st_size,
                    is_directory=item.is_dir(),
                    modified_time=stat.st_mtime
                )
                files.append(file_info)
            except (OSError, PermissionError):
                continue  # 忽略无法访问的文件
        
        return sorted(files, key=lambda x: (not x.is_directory, x.name.lower()))
    
    def create_disk_image(self, path: str, size_gb: int) -> bool:
        """创建虚拟磁盘镜像"""
        try:
            # 确保目录存在
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                'qemu-img', 'create',
                '-f', 'qcow2',
                path,
                f'{size_gb}G'
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"创建磁盘镜像失败: {e}")
            return False
        except Exception as e:
            print(f"创建磁盘镜像失败: {e}")
            return False
    
    def resize_disk_image(self, path: str, new_size_gb: int) -> bool:
        """调整虚拟磁盘大小"""
        try:
            cmd = [
                'qemu-img', 'resize',
                path,
                f'{new_size_gb}G'
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"调整磁盘大小失败: {e}")
            return False
        except Exception as e:
            print(f"调整磁盘大小失败: {e}")
            return False
    
    def convert_disk_format(self, source_path: str, target_path: str, target_format: str) -> bool:
        """转换磁盘格式"""
        try:
            cmd = [
                'qemu-img', 'convert',
                '-f', 'qcow2',  # 假设源格式为qcow2
                '-O', target_format,
                source_path,
                target_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"转换磁盘格式失败: {e}")
            return False
        except Exception as e:
            print(f"转换磁盘格式失败: {e}")
            return False
    
    def get_file_size(self, path: str) -> int:
        """获取文件大小"""
        try:
            return os.path.getsize(path)
        except OSError:
            return 0
    
    def get_disk_statistics(self, vm_name: str = None) -> Dict:
        """获取磁盘统计信息"""
        stats = {
            'total_vms': 0,
            'total_disk_usage': 0,
            'largest_vm': '',
            'largest_vm_size': 0,
            'vm_count_by_size': []
        }
        
        vm_storage_path_str = self.config_manager.get_global_config("vm_storage_path")
        vm_storage_path = Path(vm_storage_path_str) if vm_storage_path_str else Path.home() / "VirtualMachines"
        
        if vm_storage_path.exists():
            vms = [d for d in vm_storage_path.iterdir() if d.is_dir()]
            stats['total_vms'] = len(vms)
            
            vm_sizes = []
            for vm_dir in vms:
                vm_size = sum(f.stat().st_size for f in vm_dir.rglob('*') if f.is_file())
                vm_sizes.append((vm_dir.name, vm_size))
                stats['total_disk_usage'] += vm_size
                
                if vm_size > stats['largest_vm_size']:
                    stats['largest_vm'] = vm_dir.name
                    stats['largest_vm_size'] = vm_size
            
            # 按大小排序虚拟机
            stats['vm_count_by_size'] = sorted(vm_sizes, key=lambda x: x[1], reverse=True)
        
        return stats
    
    def cleanup_old_snapshots(self, days_old: int = 30) -> int:
        """清理旧快照"""
        import time
        
        snapshot_location_str = self.config_manager.get_global_config("snapshot_location")
        snapshot_location = Path(snapshot_location_str) if snapshot_location_str else Path.home() / ".ltwin" / "snapshots"
        cleaned_count = 0
        
        if snapshot_location.exists():
            cutoff_time = time.time() - (days_old * 24 * 60 * 60)
            
            for snapshot_dir in snapshot_location.rglob("*"):
                if snapshot_dir.is_dir():
                    if snapshot_dir.stat().st_mtime < cutoff_time:
                        try:
                            shutil.rmtree(snapshot_dir)
                            cleaned_count += 1
                        except OSError:
                            continue  # 忽略无法删除的目录
        
        return cleaned_count
    
    def get_vm_disk_info(self, vm_name: str) -> List[FileInfo]:
        """获取特定虚拟机的磁盘文件信息"""
        vm_storage_path = Path(self.config_manager.get_global_config("vm_storage_path"))
        vm_path = vm_storage_path / vm_name
        
        if not vm_path.exists():
            return []
        
        return self.list_directory(str(vm_path))


# 全局存储管理器实例
storage_manager = None


def get_storage_manager(config_manager) -> StorageManager:
    """获取存储管理器实例"""
    global storage_manager
    if storage_manager is None:
        storage_manager = StorageManager(config_manager)
    return storage_manager