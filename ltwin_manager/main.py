#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LTWin Manager - 虚拟机管理软件
主程序入口
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent  # 修改路径以指向项目根目录
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt


def main():
    """应用程序主入口"""
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
    from ltwin_manager.app_window import MainWindow
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()