# -*- coding: utf-8 -*-
"""
主题管理器
用于管理LTWin Manager的UI主题
"""

from PyQt6.QtWidgets import QApplication, QStyleFactory
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
import json
from pathlib import Path


class ThemeManager:
    """主题管理器"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.current_theme = self.config_manager.get_global_config("theme") or "dark"
        self.themes = {
            "dark": self._get_dark_theme(),
            "light": self._get_light_theme(),
            "blue": self._get_blue_theme(),
            "warm_white": self._get_warm_white_theme(),
            "custom": self._get_custom_theme()
        }
    
    def _get_dark_theme(self):
        """获取暗色主题样式"""
        return """
        /* Dark Theme */
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QMenuBar {
            background-color: #3c3c3c;
            color: #ffffff;
            border-bottom: 1px solid #454545;
        }
        
        QMenuBar::item {
            background: transparent;
            padding: 4px 8px;
            margin: 1px;
        }
        
        QMenuBar::item:selected {
            background: #555555;
            border-radius: 3px;
        }
        
        QMenuBar::item:pressed {
            background: #666666;
            border-radius: 3px;
        }
        
        QToolBar {
            background-color: #3c3c3c;
            border: 1px solid #454545;
            spacing: 3px;
            padding: 3px;
        }
        
        QStatusBar {
            background-color: #3c3c3c;
            border-top: 1px solid #454545;
            color: #ffffff;
        }
        
        QTreeWidget {
            background-color: #2b2b2b;
            alternate-background-color: #313131;
            color: #ffffff;
            border: 1px solid #454545;
            selection-background-color: #4a4a4a;
            selection-color: #ffffff;
        }
        
        QTreeWidget::item:selected {
            background-color: #555555;
            color: #ffffff;
        }
        
        QTreeWidget::item:hover {
            background-color: #3a3a3a;
        }
        
        QHeaderView::section {
            background-color: #3c3c3c;
            color: #ffffff;
            padding: 4px;
            border: 1px solid #454545;
            font-weight: bold;
        }
        
        QPushButton {
            background-color: #4a4a4a;
            border: 1px solid #555555;
            color: #ffffff;
            padding: 5px 10px;
            border-radius: 4px;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #555555;
            border: 1px solid #666666;
        }
        
        QPushButton:pressed {
            background-color: #666666;
            border: 1px solid #777777;
        }
        
        QPushButton:disabled {
            background-color: #3c3c3c;
            color: #888888;
            border: 1px solid #454545;
        }
        
        QLineEdit {
            background-color: #3c3c3c;
            border: 1px solid #454545;
            color: #ffffff;
            padding: 4px;
            border-radius: 3px;
        }
        
        QLineEdit:focus {
            border: 1px solid #666666;
        }
        
        QTextEdit {
            background-color: #3c3c3c;
            border: 1px solid #454545;
            color: #ffffff;
            border-radius: 3px;
        }
        
        QGroupBox {
            background-color: #313131;
            border: 1px solid #454545;
            border-radius: 4px;
            margin-top: 1ex;
            padding-top: 10px;
            color: #ffffff;
            font-weight: bold;
        }
        
        QComboBox {
            background-color: #3c3c3c;
            border: 1px solid #454545;
            color: #ffffff;
            padding: 4px;
            border-radius: 3px;
            min-width: 6em;
        }
        
        QComboBox QAbstractItemView {
            background-color: #3c3c3c;
            color: #ffffff;
            selection-background-color: #4a4a4a;
            selection-color: #ffffff;
            border: 1px solid #454545;
        }
        
        QLabel {
            color: #ffffff;
        }
        
        QProgressBar {
            border: 1px solid #454545;
            background-color: #3c3c3c;
            text-align: center;
            color: #ffffff;
        }
        
        QProgressBar::chunk {
            background-color: #4CAF50;
            width: 20px;
        }
        
        QScrollBar:vertical {
            background: #313131;
            width: 15px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:vertical {
            background: #4a4a4a;
            min-height: 20px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #555555;
        }
        
        QScrollBar:horizontal {
            background: #313131;
            height: 15px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:horizontal {
            background: #4a4a4a;
            min-width: 20px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: #555555;
        }
        
        QDialog {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QTabWidget::pane {
            border: 1px solid #454545;
            background: #2b2b2b;
        }
        
        QTabBar::tab {
            background-color: #3c3c3c;
            color: #ffffff;
            padding: 6px;
            margin: 2px;
            border: 1px solid #454545;
            border-bottom-color: #454545;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: #555555;
        }
        
        QTabBar::tab:selected {
            border-color: #666666;
            border-bottom-color: #2b2b2b;
        }
        """
    
    def _get_light_theme(self):
        """获取亮色主题样式"""
        return """
        /* Light Theme */
        QMainWindow {
            background-color: #f0f0f0;
            color: #000000;
        }
        
        QMenuBar {
            background-color: #e0e0e0;
            color: #000000;
            border-bottom: 1px solid #cccccc;
        }
        
        QMenuBar::item {
            background: transparent;
            padding: 4px 8px;
            margin: 1px;
        }
        
        QMenuBar::item:selected {
            background: #d0d0d0;
            border-radius: 3px;
        }
        
        QMenuBar::item:pressed {
            background: #c0c0c0;
            border-radius: 3px;
        }
        
        QToolBar {
            background-color: #e0e0e0;
            border: 1px solid #cccccc;
            spacing: 3px;
            padding: 3px;
        }
        
        QStatusBar {
            background-color: #e0e0e0;
            border-top: 1px solid #cccccc;
            color: #000000;
        }
        
        QTreeWidget {
            background-color: #ffffff;
            alternate-background-color: #f5f5f5;
            color: #000000;
            border: 1px solid #cccccc;
            selection-background-color: #d0d0d0;
            selection-color: #000000;
        }
        
        QTreeWidget::item:selected {
            background-color: #c0c0c0;
            color: #000000;
        }
        
        QTreeWidget::item:hover {
            background-color: #e0e0e0;
        }
        
        QHeaderView::section {
            background-color: #e0e0e0;
            color: #000000;
            padding: 4px;
            border: 1px solid #cccccc;
            font-weight: bold;
        }
        
        QPushButton {
            background-color: #d0d0d0;
            border: 1px solid #cccccc;
            color: #000000;
            padding: 5px 10px;
            border-radius: 4px;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #c0c0c0;
            border: 1px solid #bbbbbb;
        }
        
        QPushButton:pressed {
            background-color: #b0b0b0;
            border: 1px solid #aaaaaa;
        }
        
        QPushButton:disabled {
            background-color: #e0e0e0;
            color: #888888;
            border: 1px solid #cccccc;
        }
        
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            color: #000000;
            padding: 4px;
            border-radius: 3px;
        }
        
        QLineEdit:focus {
            border: 1px solid #aaaaaa;
        }
        
        QTextEdit {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            color: #000000;
            border-radius: 3px;
        }
        
        QGroupBox {
            background-color: #f5f5f5;
            border: 1px solid #cccccc;
            border-radius: 4px;
            margin-top: 1ex;
            padding-top: 10px;
            color: #000000;
            font-weight: bold;
        }
        
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            color: #000000;
            padding: 4px;
            border-radius: 3px;
            min-width: 6em;
        }
        
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            color: #000000;
            selection-background-color: #d0d0d0;
            selection-color: #000000;
            border: 1px solid #cccccc;
        }
        
        QLabel {
            color: #000000;
        }
        
        QProgressBar {
            border: 1px solid #cccccc;
            background-color: #ffffff;
            text-align: center;
            color: #000000;
        }
        
        QProgressBar::chunk {
            background-color: #4CAF50;
            width: 20px;
        }
        
        QScrollBar:vertical {
            background: #f0f0f0;
            width: 15px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:vertical {
            background: #d0d0d0;
            min-height: 20px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #c0c0c0;
        }
        
        QScrollBar:horizontal {
            background: #f0f0f0;
            height: 15px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:horizontal {
            background: #d0d0d0;
            min-width: 20px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: #c0c0c0;
        }
        
        QDialog {
            background-color: #f0f0f0;
            color: #000000;
        }
        
        QTabWidget::pane {
            border: 1px solid #cccccc;
            background: #f0f0f0;
        }
        
        QTabBar::tab {
            background-color: #e0e0e0;
            color: #000000;
            padding: 6px;
            margin: 2px;
            border: 1px solid #cccccc;
            border-bottom-color: #cccccc;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: #d0d0d0;
        }
        
        QTabBar::tab:selected {
            border-color: #bbbbbb;
            border-bottom-color: #f0f0f0;
        }
        """
    
    def _get_blue_theme(self):
        """获取蓝色主题样式"""
        return """
        /* Blue Theme */
        QMainWindow {
            background-color: #e6f3ff;
            color: #003366;
        }
        
        QMenuBar {
            background-color: #0066cc;
            color: #ffffff;
            border-bottom: 1px solid #004d99;
        }
        
        QMenuBar::item {
            background: transparent;
            padding: 4px 8px;
            margin: 1px;
        }
        
        QMenuBar::item:selected {
            background: #0077ee;
            border-radius: 3px;
        }
        
        QMenuBar::item:pressed {
            background: #0055aa;
            border-radius: 3px;
        }
        
        QToolBar {
            background-color: #cce6ff;
            border: 1px solid #99ccff;
            spacing: 3px;
            padding: 3px;
        }
        
        QStatusBar {
            background-color: #0066cc;
            border-top: 1px solid #004d99;
            color: #ffffff;
        }
        
        QTreeWidget {
            background-color: #ffffff;
            alternate-background-color: #f0f8ff;
            color: #003366;
            border: 1px solid #99ccff;
            selection-background-color: #66b2ff;
            selection-color: #ffffff;
        }
        
        QTreeWidget::item:selected {
            background-color: #3399ff;
            color: #ffffff;
        }
        
        QTreeWidget::item:hover {
            background-color: #cce6ff;
        }
        
        QHeaderView::section {
            background-color: #0066cc;
            color: #ffffff;
            padding: 4px;
            border: 1px solid #004d99;
            font-weight: bold;
        }
        
        QPushButton {
            background-color: #0077ee;
            border: 1px solid #0055aa;
            color: #ffffff;
            padding: 5px 10px;
            border-radius: 4px;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #0088ff;
            border: 1px solid #0066cc;
        }
        
        QPushButton:pressed {
            background-color: #0055aa;
            border: 1px solid #004488;
        }
        
        QPushButton:disabled {
            background-color: #99ccff;
            color: #cccccc;
            border: 1px solid #66aaff;
        }
        
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #99ccff;
            color: #003366;
            padding: 4px;
            border-radius: 3px;
        }
        
        QLineEdit:focus {
            border: 1px solid #0077ee;
        }
        
        QTextEdit {
            background-color: #ffffff;
            border: 1px solid #99ccff;
            color: #003366;
            border-radius: 3px;
        }
        
        QGroupBox {
            background-color: #f0f8ff;
            border: 1px solid #99ccff;
            border-radius: 4px;
            margin-top: 1ex;
            padding-top: 10px;
            color: #003366;
            font-weight: bold;
        }
        
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #99ccff;
            color: #003366;
            padding: 4px;
            border-radius: 3px;
            min-width: 6em;
        }
        
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            color: #003366;
            selection-background-color: #66b2ff;
            selection-color: #ffffff;
            border: 1px solid #99ccff;
        }
        
        QLabel {
            color: #003366;
        }
        
        QProgressBar {
            border: 1px solid #99ccff;
            background-color: #e6f3ff;
            text-align: center;
            color: #003366;
        }
        
        QProgressBar::chunk {
            background-color: #0077ee;
            width: 20px;
        }
        
        QScrollBar:vertical {
            background: #cce6ff;
            width: 15px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:vertical {
            background: #66b2ff;
            min-height: 20px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #3399ff;
        }
        
        QScrollBar:horizontal {
            background: #cce6ff;
            height: 15px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:horizontal {
            background: #66b2ff;
            min-width: 20px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: #3399ff;
        }
        
        QDialog {
            background-color: #e6f3ff;
            color: #003366;
        }
        
        QTabWidget::pane {
            border: 1px solid #99ccff;
            background: #e6f3ff;
        }
        
        QTabBar::tab {
            background-color: #cce6ff;
            color: #003366;
            padding: 6px;
            margin: 2px;
            border: 1px solid #99ccff;
            border-bottom-color: #99ccff;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: #99ddff;
        }
        
        QTabBar::tab:selected {
            border-color: #66b2ff;
            border-bottom-color: #e6f3ff;
        }
        """
    
    def _get_warm_white_theme(self):
        """获取暖白色主题样式"""
        return """
        /* Warm White Theme */
        QMainWindow {
            background-color: #fdfdfd;
            color: #333333;
        }
        
        QMenuBar {
            background-color: #f8f8f8;
            color: #333333;
            border-bottom: 1px solid #e0e0e0;
        }
        
        QMenuBar::item {
            background: transparent;
            padding: 4px 8px;
            margin: 1px;
        }
        
        QMenuBar::item:selected {
            background: #e8e8e8;
            border-radius: 3px;
        }
        
        QMenuBar::item:pressed {
            background: #d8d8d8;
            border-radius: 3px;
        }
        
        QToolBar {
            background-color: #f8f8f8;
            border: 1px solid #e0e0e0;
            spacing: 3px;
            padding: 3px;
        }
        
        QStatusBar {
            background-color: #f8f8f8;
            border-top: 1px solid #e0e0e0;
            color: #333333;
        }
        
        QTreeWidget {
            background-color: #ffffff;
            alternate-background-color: #fafafa;
            color: #333333;
            border: 1px solid #e0e0e0;
            selection-background-color: #e0e8f0;
            selection-color: #000000;
        }
        
        QTreeWidget::item:selected {
            background-color: #d0ddf0;
            color: #000000;
        }
        
        QTreeWidget::item:hover {
            background-color: #f0f0f0;
        }
        
        QHeaderView::section {
            background-color: #f0f0f0;
            color: #333333;
            padding: 4px;
            border: 1px solid #e0e0e0;
            font-weight: bold;
        }
        
        QPushButton {
            background-color: #f0f0f0;
            border: 1px solid #d0d0d0;
            color: #333333;
            padding: 5px 10px;
            border-radius: 4px;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #e8e8e8;
            border: 1px solid #c0c0c0;
        }
        
        QPushButton:pressed {
            background-color: #d0d0d0;
            border: 1px solid #b0b0b0;
        }
        
        QPushButton:disabled {
            background-color: #f5f5f5;
            color: #a0a0a0;
            border: 1px solid #e0e0e0;
        }
        
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #d0d0d0;
            color: #333333;
            padding: 4px;
            border-radius: 3px;
        }
        
        QLineEdit:focus {
            border: 1px solid #a0c4ff;
        }
        
        QTextEdit {
            background-color: #ffffff;
            border: 1px solid #d0d0d0;
            color: #333333;
            border-radius: 3px;
        }
        
        QGroupBox {
            background-color: #fafafa;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            margin-top: 1ex;
            padding-top: 10px;
            color: #333333;
            font-weight: bold;
        }
        
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #d0d0d0;
            color: #333333;
            padding: 4px;
            border-radius: 3px;
            min-width: 6em;
        }
        
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            color: #333333;
            selection-background-color: #e0e8f0;
            selection-color: #000000;
            border: 1px solid #d0d0d0;
        }
        
        QLabel {
            color: #333333;
        }
        
        QProgressBar {
            border: 1px solid #e0e0e0;
            background-color: #fafafa;
            text-align: center;
            color: #333333;
        }
        
        QProgressBar::chunk {
            background-color: #4a90e2;
            width: 20px;
        }
        
        QScrollBar:vertical {
            background: #f8f8f8;
            width: 15px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:vertical {
            background: #e0e0e0;
            min-height: 20px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #d0d0d0;
        }
        
        QScrollBar:horizontal {
            background: #f8f8f8;
            height: 15px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:horizontal {
            background: #e0e0e0;
            min-width: 20px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: #d0d0d0;
        }
        
        QDialog {
            background-color: #fdfdfd;
            color: #333333;
        }
        
        QTabWidget::pane {
            border: 1px solid #e0e0e0;
            background: #fdfdfd;
        }
        
        QTabBar::tab {
            background-color: #f8f8f8;
            color: #333333;
            padding: 6px;
            margin: 2px;
            border: 1px solid #e0e0e0;
            border-bottom-color: #e0e0e0;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: #e8e8e8;
        }
        
        QTabBar::tab:selected {
            border-color: #d0d0d0;
            border-bottom-color: #fdfdfd;
        }
        """

    def _get_custom_theme(self):
        """获取自定义主题样式（默认为暗色）"""
        # 从配置文件加载自定义主题
        theme_file = Path.home() / ".ltwin" / "custom_theme.qss"
        if theme_file.exists():
            try:
                with open(theme_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except:
                pass
        return self._get_dark_theme()
    
    def apply_theme(self, app):
        """应用当前主题到应用程序"""
        if self.current_theme in self.themes:
            app.setStyleSheet(self.themes[self.current_theme])
        else:
            app.setStyleSheet(self.themes["dark"])  # 默认使用暗色主题
    
    def set_theme(self, theme_name):
        """设置新主题"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.config_manager.set_global_config("theme", theme_name)
            return True
        return False
    
    def get_available_themes(self):
        """获取可用主题列表"""
        return list(self.themes.keys())


# 全局主题管理器实例
theme_manager = None


def get_theme_manager(config_manager) -> ThemeManager:
    """获取主题管理器实例"""
    global theme_manager
    if theme_manager is None:
        theme_manager = ThemeManager(config_manager)
    return theme_manager