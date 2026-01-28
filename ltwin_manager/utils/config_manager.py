# -*- coding: utf-8 -*-
"""
配置管理器
用于管理LTWin Manager的全局配置、虚拟机配置和镜像配置
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import shutil


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        # 配置文件路径
        self.config_dir = Path.home() / '.ltwin'
        self.global_config_path = self.config_dir / 'config.json'
        self.vms_config_path = self.config_dir / 'vms.json'
        self.images_config_path = self.config_dir / 'images.json'
        
        # 确保配置目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化配置
        self.global_config = self._load_global_config()
        self.vms_config = self._load_vms_config()
        self.images_config = self._load_images_config()
    
    def _load_global_config(self) -> Dict[str, Any]:
        """加载全局配置"""
        if self.global_config_path.exists():
            try:
                with open(self.global_config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载全局配置失败: {e}")
        
        # 默认配置
        default_config = {
            "default_vm_cpu_cores": 2,
            "default_vm_memory_mb": 2048,
            "default_vm_disk_size_gb": 20,
            "vm_storage_path": str(Path.home() / "VirtualMachines"),
            "iso_storage_path": str(Path.home() / "ISOFiles"),
            "vnc_base_port": 5900,
            "language": "zh-CN",
            "theme": "warm_white",
            "auto_check_updates": True,
            "show_tray_icon": True,
            "check_kvm_support": True,
            "auto_optimize_vm": True,
            "max_concurrent_vms": 5,
            "enable_snapshots": True,
            "snapshot_location": str(Path.home() / "VM_Snapshots")
        }
        
        self._save_global_config(default_config)
        return default_config
    
    def _save_global_config(self, config: Dict[str, Any]) -> bool:
        """保存全局配置"""
        try:
            with open(self.global_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self.global_config = config
            return True
        except Exception as e:
            print(f"保存全局配置失败: {e}")
            return False
    
    def _load_vms_config(self) -> Dict[str, Any]:
        """加载虚拟机配置"""
        if self.vms_config_path.exists():
            try:
                with open(self.vms_config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载虚拟机配置失败: {e}")
        
        return {}  # 返回空字典而不是默认配置
    
    def _save_vms_config(self, config: Dict[str, Any]) -> bool:
        """保存虚拟机配置"""
        try:
            with open(self.vms_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self.vms_config = config
            return True
        except Exception as e:
            print(f"保存虚拟机配置失败: {e}")
            return False
    
    def _load_images_config(self) -> Dict[str, Any]:
        """加载镜像配置"""
        if self.images_config_path.exists():
            try:
                with open(self.images_config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载镜像配置失败: {e}")
        
        return {}
    
    def _save_images_config(self, config: Dict[str, Any]) -> bool:
        """保存镜像配置"""
        try:
            with open(self.images_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self.images_config = config
            return True
        except Exception as e:
            print(f"保存镜像配置失败: {e}")
            return False
    
    # 全局配置相关方法
    def get_global_config(self, key: str = None) -> Any:
        """获取全局配置值"""
        if key:
            value = self.global_config.get(key)
            # 如果配置中没有该键且有默认值，则返回默认值
            if value is None:
                default_values = {
                    "default_vm_cpu_cores": 2,
                    "default_vm_memory_mb": 2048,
                    "default_vm_disk_size_gb": 20,
                    "vm_storage_path": str(Path.home() / "VirtualMachines"),
                    "iso_storage_path": str(Path.home() / "ISOFiles"),
                    "vnc_base_port": 5900,
                    "language": "zh-CN",
                    "theme": "warm_white",
                    "auto_check_updates": True,
                    "show_tray_icon": True,
                    "check_kvm_support": True,
                    "auto_optimize_vm": True,
                    "max_concurrent_vms": 5,
                    "enable_snapshots": True,
                    "snapshot_location": str(Path.home() / "VM_Snapshots")
                }
                if key in default_values:
                    return default_values[key]
            return value
        return self.global_config
    
    def set_global_config(self, key: str, value: Any) -> bool:
        """设置全局配置值"""
        self.global_config[key] = value
        return self._save_global_config(self.global_config)
    
    def update_global_config(self, updates: Dict[str, Any]) -> bool:
        """批量更新全局配置"""
        self.global_config.update(updates)
        return self._save_global_config(self.global_config)
    
    # 虚拟机配置相关方法
    def get_vm_config(self, vm_name: str) -> Optional[Dict[str, Any]]:
        """获取虚拟机配置"""
        return self.vms_config.get(vm_name)
    
    def set_vm_config(self, vm_name: str, config: Dict[str, Any]) -> bool:
        """设置虚拟机配置"""
        self.vms_config[vm_name] = config
        return self._save_vms_config(self.vms_config)
    
    def delete_vm_config(self, vm_name: str) -> bool:
        """删除虚拟机配置"""
        if vm_name in self.vms_config:
            del self.vms_config[vm_name]
            return self._save_vms_config(self.vms_config)
        return False
    
    def list_vms(self) -> List[str]:
        """列出所有虚拟机"""
        return list(self.vms_config.keys())
    
    def vm_exists(self, vm_name: str) -> bool:
        """检查虚拟机是否存在"""
        return vm_name in self.vms_config
    
    # 镜像配置相关方法
    def get_image_config(self, image_name: str) -> Optional[Dict[str, Any]]:
        """获取镜像配置"""
        return self.images_config.get(image_name)
    
    def set_image_config(self, image_name: str, config: Dict[str, Any]) -> bool:
        """设置镜像配置"""
        self.images_config[image_name] = config
        return self._save_images_config(self.images_config)
    
    def delete_image_config(self, image_name: str) -> bool:
        """删除镜像配置"""
        if image_name in self.images_config:
            del self.images_config[image_name]
            return self._save_images_config(self.images_config)
        return False
    
    def list_images(self) -> List[str]:
        """列出所有镜像"""
        return list(self.images_config.keys())
    
    def image_exists(self, image_name: str) -> bool:
        """检查镜像是否存在"""
        return image_name in self.images_config
    
    # 便捷方法
    def get_default_vm_storage_path(self) -> Path:
        """获取默认虚拟机存储路径"""
        path_str = self.global_config.get("vm_storage_path", str(Path.home() / "VirtualMachines"))
        return Path(path_str)
    
    def get_default_iso_storage_path(self) -> Path:
        """获取默认ISO存储路径"""
        path_str = self.global_config.get("iso_storage_path", str(Path.home() / "ISOFiles"))
        return Path(path_str)
    
    def get_next_vnc_port(self) -> int:
        """获取下一个可用的VNC端口"""
        used_ports = []
        for vm_config in self.vms_config.values():
            if 'vnc_port' in vm_config:
                used_ports.append(vm_config['vnc_port'])
        
        base_port = self.global_config.get("vnc_base_port", 5900)
        port = base_port + 1  # 从基础端口+1开始
        
        while port in used_ports:
            port += 1
        
        return port
    
    def export_config(self, backup_path: str) -> bool:
        """导出配置到备份文件"""
        try:
            backup_data = {
                'global': self.global_config,
                'vms': self.vms_config,
                'images': self.images_config
            }
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"导出配置失败: {e}")
            return False
    
    def import_config(self, backup_path: str) -> bool:
        """从备份文件导入配置"""
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            if 'global' in backup_data:
                self._save_global_config(backup_data['global'])
            
            if 'vms' in backup_data:
                self._save_vms_config(backup_data['vms'])
            
            if 'images' in backup_data:
                self._save_images_config(backup_data['images'])
            
            return True
        except Exception as e:
            print(f"导入配置失败: {e}")
            return False


# 全局配置管理器实例
config_manager = ConfigManager()


def get_config_manager() -> ConfigManager:
    """获取配置管理器实例"""
    return config_manager


if __name__ == "__main__":
    # 测试配置管理器
    cm = get_config_manager()
    
    print("全局配置:")
    print(json.dumps(cm.get_global_config(), ensure_ascii=False, indent=2))
    
    print(f"\n虚拟机存储路径: {cm.get_default_vm_storage_path()}")
    print(f"ISO存储路径: {cm.get_default_iso_storage_path()}")
    
    print(f"\n现有虚拟机: {cm.list_vms()}")
    print(f"现有镜像: {cm.list_images()}")