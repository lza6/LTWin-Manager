#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LTWin Manager 启动器
用于启动LTWin Manager应用
"""

import sys
import os
from pathlib import Path


def main():
    """启动LTWin Manager"""
    # 添加项目根目录到Python路径
    project_root = Path(__file__).parent
    ltwin_manager_path = project_root / "ltwin_manager"
    
    if ltwin_manager_path.exists():
        sys.path.insert(0, str(project_root))
        
        try:
            from ltwin_manager.main import main as ltwin_main
            ltwin_main()
        except ImportError as e:
            print(f"导入错误: {e}")
            print("请确保已运行 setup_project.py 初始化项目")
            
            # 尝试运行初始化
            setup_script = project_root / "setup_project.py"
            if setup_script.exists():
                import subprocess
                print("正在运行项目初始化...")
                result = subprocess.run([sys.executable, str(setup_script)])
                if result.returncode == 0:
                    print("初始化完成，正在启动应用...")
                    try:
                        from ltwin_manager.main import main as ltwin_main
                        ltwin_main()
                    except ImportError as e2:
                        print(f"仍然无法启动: {e2}")
                        input("按回车键退出...")
            else:
                input("setup_project.py 不存在，请先创建此文件。按回车键退出...")
        except Exception as e:
            print(f"启动错误: {e}")
            import traceback
            traceback.print_exc()
            input("按回车键退出...")
    else:
        print("错误: ltwin_manager 目录不存在")
        print("请先运行 setup_project.py 初始化项目")
        input("按回车键退出...")


if __name__ == "__main__":
    main()