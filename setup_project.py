#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LTWin Manager 项目初始化脚本
用于验证安装和依赖关系
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("错误: Python版本过低，需要Python 3.8或更高版本")
        return False
    print(f"✓ Python版本检查通过: {sys.version.split()[0]}")
    return True

def check_and_install_package(package_name, import_name=None):
    """检查并安装包"""
    if import_name is None:
        import_name = package_name
        
    try:
        # 尝试导入
        importlib.import_module(import_name)
        print(f"✓ {package_name} 已安装")
        return True
    except ImportError:
        print(f"- {package_name} 未安装，正在尝试安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✓ {package_name} 安装成功")
            return True
        except subprocess.CalledProcessError:
            print(f"✗ {package_name} 安装失败")
            return False

def check_dependencies():
    """检查所有依赖"""
    print("\n正在检查依赖...")
    
    required_packages = [
        ("PyQt6", "PyQt6"),
        ("PyQt6-sip", "PyQt6.sip"),
        ("psutil", "psutil"),
        ("requests", "requests"),
        ("SQLAlchemy", "sqlalchemy"),
        ("paramiko", "paramiko")
    ]
    
    all_installed = True
    for pkg_name, import_name in required_packages:
        if not check_and_install_package(pkg_name, import_name):
            all_installed = False
    
    return all_installed

def check_qemu():
    """检查QEMU是否已安装"""
    try:
        result = subprocess.run(['qemu-system-x86_64', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✓ QEMU已安装: {result.stdout.split()[2] if len(result.stdout.split()) > 2 else 'unknown version'}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    
    print("? QEMU未安装 - 可选组件，用于虚拟机功能")
    print("  提示: 请从 https://www.qemu.org/download/ 安装QEMU以支持虚拟机功能")
    return False

def create_requirements_file():
    """创建requirements.txt文件"""
    requirements = [
        "PyQt6>=6.4.0",
        "PyQt6-Qt6>=6.4.0",
        "PyQt6-sip>=13.4.0",
        "psutil>=5.9.0",
        "requests>=2.28.0",
        "SQLAlchemy>=2.0.0",
        "paramiko>=3.0.0"
    ]
    
    with open("requirements.txt", "w", encoding="utf-8") as f:
        for req in requirements:
            f.write(req + "\n")
    
    print("✓ requirements.txt 已创建")

def verify_project_structure():
    """验证项目结构"""
    print("\n正在验证项目结构...")
    
    required_dirs = [
        "ltwin_manager",
        "ltwin_manager/ui",
        "ltwin_manager/ui/dialogs",
        "ltwin_manager/controllers",
        "ltwin_manager/models",
        "ltwin_manager/utils"
    ]
    
    required_files = [
        "ltwin_manager/__init__.py",
        "ltwin_manager/main.py",
        "ltwin_manager/app_window.py",
        "run_ltwin.py",
        "quick_start.bat"
    ]
    
    all_exist = True
    
    for directory in required_dirs:
        if not os.path.isdir(directory):
            print(f"✗ 目录不存在: {directory}")
            all_exist = False
        else:
            print(f"✓ 目录存在: {directory}")
    
    for filename in required_files:
        if not os.path.isfile(filename):
            print(f"✗ 文件不存在: {filename}")
            all_exist = False
        else:
            print(f"✓ 文件存在: {filename}")
    
    return all_exist

def main():
    """主函数"""
    print("=" * 60)
    print("LTWin Manager - 项目初始化和验证脚本")
    print("=" * 60)
    
    # 检查Python版本
    if not check_python_version():
        return 1
    
    # 创建requirements.txt
    create_requirements_file()
    
    # 检查依赖
    deps_ok = check_dependencies()
    
    # 检查QEMU
    qemu_ok = check_qemu()
    
    # 验证项目结构
    structure_ok = verify_project_structure()
    
    print("\n" + "=" * 60)
    print("验证结果摘要:")
    print(f"  Python版本检查: {'通过' if check_python_version() else '失败'}")
    print(f"  依赖检查: {'通过' if deps_ok else '失败'}")
    print(f"  QEMU检查: {'已安装' if qemu_ok else '未安装'}")
    print(f"  项目结构: {'正确' if structure_ok else '存在问题'}")
    
    if deps_ok and structure_ok:
        print("\n✓ 项目验证成功！LTWin Manager可以正常运行。")
        print("\n要启动LTWin Manager，请运行:")
        print("  python run_ltwin.py")
        print("\n或者使用快速启动脚本:")
        print("  quick_start.bat")
    else:
        print("\n✗ 项目验证失败，请根据上述信息解决问题后重试。")
        return 1
    
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())