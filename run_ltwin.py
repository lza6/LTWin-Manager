#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LTWin Manager - 虚拟机管理软件
增强型主程序入口
包含依赖检查和错误处理
"""

import sys
import os
import subprocess
import traceback
from pathlib import Path

def check_dependencies():
    """检查必需的依赖"""
    missing_deps = []
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("错误: Python版本过低，需要Python 3.8或更高版本")
        return False
    
    # 检查PyQt6
    try:
        import PyQt6
    except ImportError:
        missing_deps.append("PyQt6")
    
    # 检查psutil
    try:
        import psutil
    except ImportError:
        missing_deps.append("psutil")
    
    # 检查requests
    try:
        import requests
    except ImportError:
        missing_deps.append("requests")
    
    # 检查SQLAlchemy
    try:
        import sqlalchemy
    except ImportError:
        missing_deps.append("SQLAlchemy")
    
    if missing_deps:
        print(f"缺少依赖: {', '.join(missing_deps)}")
        print("正在尝试安装缺失的依赖...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_deps)
            print("依赖安装成功")
            return True
        except subprocess.CalledProcessError:
            print("无法自动安装依赖，请手动安装:")
            for dep in missing_deps:
                print(f"  pip install {dep}")
            return False
    
    return True

def check_qemu():
    """检查QEMU是否已安装"""
    try:
        result = subprocess.run(['qemu-system-x86_64', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"QEMU已安装: {result.stdout.split()[2] if len(result.stdout.split()) > 2 else 'unknown version'}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    
    print("警告: 未找到QEMU虚拟化工具")
    print("提示: 请安装QEMU以支持虚拟机功能")
    print("下载地址: https://www.qemu.org/download/")
    return False

def main():
    """应用程序主入口，带有错误处理和依赖检查"""
    print("=" * 50)
    print("LTWin Manager 启动")
    print("脚本开始执行")
    print("=" * 50)
    
    print(f"Python版本检查通过\n: {sys.version.split()[0]}")
    
    # 检查依赖
    if not check_dependencies():
        print("依赖检查失败，程序无法启动")
        input("\n按回车键退出...")
        return 1
    
    # 检查QEMU
    check_qemu()
    
    print("\n开始启动LTWin Manager...")
    
    try:
        # 添加项目根目录到Python路径
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        from ltwin_manager.app_window import MainWindow
        
        # 设置高DPI缩放支持
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        
        app = QApplication(sys.argv)
        app.setApplicationName("LTWin Manager")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("LTWin Project")
        
        # 应用主题
        from ltwin_manager.utils.theme_manager import get_theme_manager
        from ltwin_manager.utils.config_manager import get_config_manager
        config_manager = get_config_manager()
        theme_manager = get_theme_manager(config_manager)
        theme_manager.apply_theme(app)
        
        # 创建并显示主窗口
        window = MainWindow()
        window.show()
        
        print("LTWin Manager 启动成功")
        print("应用程序正在运行...")
        
        result = app.exec()
        print("LTWin Manager 已退出")
        return result
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("这可能是由于缺少依赖或模块路径问题")
        print("请确保已正确安装所有依赖")
        traceback.print_exc()
        input("\n按回车键退出...")
        return 1
    except Exception as e:
        print(f"启动过程中发生错误: {e}")
        print("详细错误信息:")
        traceback.print_exc()
        input("\n按回车键退出...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
