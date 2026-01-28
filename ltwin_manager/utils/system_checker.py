# -*- coding: utf-8 -*-
"""
系统检测和修复工具
用于检测系统环境并自动修复缺失的组件
"""

import subprocess
import sys
import os
import platform
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import requests
import tempfile
import threading
from PyQt6.QtCore import QObject, pyqtSignal


class SystemChecker(QObject):
    """系统检测器"""
    
    # 信号定义
    check_progress = pyqtSignal(str, int)  # 检测进度: (状态消息, 进度百分比)
    repair_progress = pyqtSignal(str, int)  # 修复进度: (状态消息, 进度百分比)
    repair_complete = pyqtSignal(bool)  # 修复完成: (是否成功)
    
    def __init__(self):
        super().__init__()
        self.missing_components = []
        self.system_info = {}
    
    def detect_system_info(self) -> Dict:
        """检测系统信息"""
        self.check_progress.emit("检测系统信息...", 5)
        
        info = {
            'os': platform.system(),
            'os_version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'python_path': sys.executable,
        }
        
        # 检测内存
        try:
            import psutil
            memory = psutil.virtual_memory()
            info['total_memory_gb'] = round(memory.total / (1024**3), 2)
            info['available_memory_gb'] = round(memory.available / (1024**3), 2)
        except ImportError:
            info['total_memory_gb'] = '未知'
            info['available_memory_gb'] = '未知'
        
        # 检测磁盘空间
        try:
            disk_usage = os.path.exists('.') and os.statvfs('.') if hasattr(os, 'statvfs') else None
            if disk_usage:
                info['disk_space_gb'] = round(disk_usage.f_frsize * disk_usage.f_bavail / (1024**3), 2)
            else:
                # Windows兼容方案
                import shutil
                total, used, free = shutil.disk_usage('.')
                info['disk_space_gb'] = round(free / (1024**3), 2)
        except:
            info['disk_space_gb'] = '未知'
        
        self.system_info = info
        return info
    
    def check_dependencies(self) -> Dict[str, bool]:
        """检查依赖项"""
        self.check_progress.emit("检查Python依赖...", 10)
        
        dependencies = {
            'python': self._check_python(),
            'pip': self._check_pip(),
            'pyqt6': self._check_pyqt6(),
            'psutil': self._check_psutil(),
            'requests': self._check_requests(),
            'qemu': self._check_qemu(),
            'qemu_img': self._check_qemu_img(),
        }
        
        # 检查其他可能的依赖
        additional_checks = [
            ('sqlalchemy', lambda: self._check_module('SQLAlchemy')),
            ('paramiko', lambda: self._check_module('paramiko')),
        ]
        
        for name, check_func in additional_checks:
            self.check_progress.emit(f"检查{name}...", 15)
            dependencies[name] = check_func()
        
        # 收集缺失的组件
        self.missing_components = [name for name, installed in dependencies.items() if not installed]
        
        return dependencies
    
    def _check_python(self) -> bool:
        """检查Python版本"""
        try:
            major, minor = sys.version_info[:2]
            return major >= 3 and minor >= 8
        except:
            return False
    
    def _check_pip(self) -> bool:
        """检查pip"""
        try:
            subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                          check=True, capture_output=True)
            return True
        except:
            return False
    
    def _check_pyqt6(self) -> bool:
        """检查PyQt6"""
        try:
            import PyQt6
            return True
        except ImportError:
            return False
    
    def _check_psutil(self) -> bool:
        """检查psutil"""
        try:
            import psutil
            return True
        except ImportError:
            return False
    
    def _check_requests(self) -> bool:
        """检查requests"""
        try:
            import requests
            return True
        except ImportError:
            return False
    
    def _check_qemu(self) -> bool:
        """检查QEMU"""
        try:
            result = subprocess.run(['qemu-system-x86_64', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
        except:
            return False
    
    def _check_qemu_img(self) -> bool:
        """检查qemu-img"""
        try:
            result = subprocess.run(['qemu-img', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
        except:
            return False
    
    def _check_module(self, module_name: str) -> bool:
        """检查Python模块"""
        try:
            __import__(module_name.lower() if module_name.lower() in ['pillow'] else module_name.replace('-', '_'))
            return True
        except ImportError:
            return False
    
    def check_virtualization_support(self) -> bool:
        """检查虚拟化支持"""
        self.check_progress.emit("检查虚拟化支持...", 20)
        
        if platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ["wmic", "cpu", "get", "VirtualizationFirmwareEnabled"], 
                    capture_output=True, text=True
                )
                return "TRUE" in result.stdout
            except:
                # 备选方案：检查Hyper-V是否启用
                try:
                    result = subprocess.run(
                        ["systeminfo", "|", "findstr", "Hyper-V"], 
                        shell=True, capture_output=True, text=True
                    )
                    return True  # 如果命令成功执行，认为支持虚拟化
                except:
                    return True  # 不确定的情况下，假设支持
        elif platform.system() == "Linux":
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read()
                    return 'vmx' in cpuinfo or 'svm' in cpuinfo
            except:
                return True  # 不确定的情况下，假设支持
        else:
            return True  # 其他系统假设支持
    
    def run_comprehensive_check(self) -> Dict:
        """运行综合检查"""
        try:
            # 检测系统信息
            system_info = self.detect_system_info()
            
            # 检查依赖
            dependencies = self.check_dependencies()
            
            # 检查虚拟化支持
            virtualization_supported = self.check_virtualization_support()
            
            self.check_progress.emit("检查完成", 100)
            
            return {
                'system_info': system_info,
                'dependencies': dependencies,
                'virtualization_supported': virtualization_supported,
                'missing_components': self.missing_components.copy()
            }
        except Exception as e:
            self.check_progress.emit(f"检查出错: {str(e)}", 100)
            return {
                'system_info': {},
                'dependencies': {},
                'virtualization_supported': False,
                'missing_components': [],
                'error': str(e)
            }
    
    def repair_missing_components(self) -> bool:
        """修复缺失的组件"""
        if not self.missing_components:
            self.repair_progress.emit("没有需要修复的组件", 100)
            return True
        
        total_components = len(self.missing_components)
        progress_per_component = 80 // total_components if total_components > 0 else 0
        
        success_count = 0
        for i, component in enumerate(self.missing_components):
            self.repair_progress.emit(f"正在修复 {component}...", i * progress_per_component)
            
            try:
                if component == 'python':
                    self.repair_progress.emit("请手动安装Python 3.8或更高版本", i * progress_per_component)
                elif component == 'pip':
                    self._repair_pip()
                elif component in ['pyqt6', 'psutil', 'requests', 'sqlalchemy', 'paramiko']:
                    self._repair_python_package(component)
                elif component in ['qemu', 'qemu_img']:
                    self._repair_qemu()
                else:
                    # 默认尝试作为Python包修复
                    self._repair_python_package(component)
                
                success_count += 1
                self.repair_progress.emit(f"已修复 {component}", (i + 1) * progress_per_component)
                
            except Exception as e:
                self.repair_progress.emit(f"修复 {component} 失败: {str(e)}", (i + 1) * progress_per_component)
        
        # 最终验证
        self.repair_progress.emit("验证修复结果...", 90)
        remaining_missing = self._verify_repair()
        
        final_success = len(remaining_missing) == 0
        self.repair_progress.emit("修复完成" if final_success else f"修复完成，仍有 {len(remaining_missing)} 个组件未修复", 100)
        
        self.repair_complete.emit(final_success)
        return final_success
    
    def _repair_pip(self):
        """修复pip"""
        try:
            subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'], check=True)
        except:
            # 如果ensurepip失败，尝试其他方法
            subprocess.run([sys.executable, '-m', 'urllib.request', 'https://bootstrap.pypa.io/get-pip.py', '-o', 'get-pip.py'])
            subprocess.run([sys.executable, 'get-pip.py'])
            if os.path.exists('get-pip.py'):
                os.remove('get-pip.py')
    
    def _repair_python_package(self, package_name: str):
        """修复Python包"""
        # 映射包名到正确的安装名称
        package_map = {
            'pyqt6': 'PyQt6',
            'psutil': 'psutil',
            'requests': 'requests',
            'sqlalchemy': 'SQLAlchemy',
            'paramiko': 'paramiko',
        }
        
        install_name = package_map.get(package_name, package_name)
        subprocess.run([sys.executable, '-m', 'pip', 'install', install_name], check=True)
    
    def _repair_qemu(self):
        """修复QEMU（仅提供下载链接，因为安装较复杂）"""
        # 对于QEMU，我们只能提供下载链接
        if platform.system() == "Windows":
            self.repair_progress.emit("请从 https://www.qemu.org/download/#windows 下载并安装QEMU", 50)
        else:
            self.repair_progress.emit(f"请使用系统包管理器安装QEMU (例如: sudo apt install qemu)", 50)
    
    def _verify_repair(self) -> List[str]:
        """验证修复结果"""
        # 重新检查之前缺失的组件
        still_missing = []
        for component in self.missing_components:
            if component == 'python':
                if not self._check_python():
                    still_missing.append(component)
            elif component == 'pip':
                if not self._check_pip():
                    still_missing.append(component)
            elif component in ['pyqt6', 'psutil', 'requests', 'sqlalchemy', 'paramiko']:
                if not self._check_module(component.replace('pyqt6', 'PyQt6')):
                    still_missing.append(component)
            elif component in ['qemu', 'qemu_img']:
                if component == 'qemu' and not self._check_qemu():
                    still_missing.append(component)
                elif component == 'qemu_img' and not self._check_qemu_img():
                    still_missing.append(component)
        
        return still_missing


def run_system_check():
    """运行系统检查的便捷函数"""
    checker = SystemChecker()
    return checker.run_comprehensive_check()


if __name__ == "__main__":
    # 测试系统检查功能
    result = run_system_check()
    
    print("=== 系统检查结果 ===")
    print(f"系统信息: {result['system_info']}")
    print(f"依赖状态: {result['dependencies']}")
    print(f"虚拟化支持: {result['virtualization_supported']}")
    print(f"缺失组件: {result['missing_components']}")
    
    if result.get('error'):
        print(f"错误: {result['error']}")