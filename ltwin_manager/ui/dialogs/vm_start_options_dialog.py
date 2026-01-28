"""
虚拟机启动选项对话框
"""

import sys
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QGroupBox, 
                             QFormLayout, QApplication, QWidget, QCheckBox, QSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class VMStartOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('虚拟机启动选项')
        self.setModal(True)
        self.resize(500, 400)
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel('配置虚拟机启动参数')
        title_label.setFont(QFont('Microsoft YaHei', 12, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # 基本配置
        basic_group = QGroupBox('基本配置')
        basic_layout = QFormLayout()
        
        self.cpu_count = QSpinBox()
        self.cpu_count.setRange(1, 32)
        self.cpu_count.setValue(6)
        basic_layout.addRow('CPU核心数:', self.cpu_count)
        
        self.memory_size = QSpinBox()
        self.memory_size.setRange(1, 64)
        self.memory_size.setValue(12)
        self.memory_size.setSuffix(' GB')
        basic_layout.addRow('内存大小:', self.memory_size)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # 磁盘配置
        disk_group = QGroupBox('磁盘配置')
        disk_layout = QFormLayout()
        
        self.system_disk_path = QLineEdit(os.path.join(os.getcwd(), 'win10.vmdk'))
        disk_layout.addRow('系统磁盘:', self.system_disk_path)
        
        disk_group.setLayout(disk_layout)
        layout.addWidget(disk_group)
        
        # 网络配置
        net_group = QGroupBox('网络配置')
        net_layout = QFormLayout()
        
        self.network_mode = QLineEdit('user')
        net_layout.addRow('网络模式:', self.network_mode)
        
        net_group.setLayout(net_layout)
        layout.addWidget(net_group)
        
        # VNC配置
        vnc_group = QGroupBox('VNC配置')
        vnc_layout = QFormLayout()
        
        self.vnc_port = QSpinBox()
        self.vnc_port.setRange(0, 10)
        self.vnc_port.setValue(2)
        vnc_layout.addRow('VNC端口 (:号):', self.vnc_port)
        
        vnc_group.setLayout(vnc_layout)
        layout.addWidget(vnc_group)
        
        # 启动ISO选项
        iso_group = QGroupBox('启动ISO')
        iso_layout = QFormLayout()
        
        self.boot_iso_path = QLineEdit('')
        iso_layout.addRow('启动ISO (可选):', self.boot_iso_path)
        
        iso_group.setLayout(iso_layout)
        layout.addWidget(iso_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        self.ok_btn = QPushButton('启动')
        self.ok_btn.clicked.connect(self.accept)
        
        self.cancel_btn = QPushButton('取消')
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = VMStartOptionsDialog()
    dialog.exec()
    sys.exit(app.exec())