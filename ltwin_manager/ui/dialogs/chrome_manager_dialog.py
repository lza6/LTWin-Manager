"""
Chrome安装管理对话框
"""

import sys
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QGroupBox, 
                             QFormLayout, QApplication, QWidget, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ChromeManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Chrome安装管理')
        self.setModal(True)
        self.resize(500, 300)
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel('管理Chrome安装镜像')
        title_label.setFont(QFont('Microsoft YaHei', 12, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # Chrome ISO路径
        iso_group = QGroupBox('Chrome安装镜像')
        iso_layout = QFormLayout()
        
        self.chrome_iso_path = QLineEdit(os.path.join(os.getcwd(), 'Chrome.iso'))
        iso_layout.addRow('ISO文件路径:', self.chrome_iso_path)
        
        self.chrome_url = QLineEdit('https://archive.org/download/chrome_20240526/Chrome.iso')
        iso_layout.addRow('下载地址:', self.chrome_url)
        
        iso_group.setLayout(iso_layout)
        layout.addWidget(iso_group)
        
        # 操作选项
        options_group = QGroupBox('操作选项')
        options_layout = QVBoxLayout()
        
        self.mount_checkbox = QCheckBox('启动时挂载Chrome ISO')
        self.mount_checkbox.setChecked(True)
        options_layout.addWidget(self.mount_checkbox)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # 状态显示
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        self.check_btn = QPushButton('检查ISO')
        self.check_btn.clicked.connect(self.check_iso)
        
        self.download_btn = QPushButton('下载ISO')
        self.download_btn.clicked.connect(self.download_iso)
        
        self.ok_btn = QPushButton('确定')
        self.ok_btn.clicked.connect(self.accept)
        
        self.cancel_btn = QPushButton('取消')
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.check_btn)
        button_layout.addWidget(self.download_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def check_iso(self):
        """检查ISO文件是否存在"""
        iso_path = self.chrome_iso_path.text()
        if os.path.exists(iso_path):
            self.status_text.append(f'找到Chrome ISO: {iso_path}')
        else:
            self.status_text.append(f'未找到Chrome ISO: {iso_path}')
    
    def download_iso(self):
        """下载Chrome ISO"""
        self.status_text.append('正在下载Chrome ISO...')
        # TODO: 实现实际的下载逻辑
        self.status_text.append('下载完成')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = ChromeManagerDialog()
    dialog.exec()
    sys.exit(app.exec())