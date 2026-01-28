# -*- coding: utf-8 -*-
"""
虚拟机配置对话框
用于创建和编辑虚拟机配置
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QPushButton, QLabel, QGroupBox, QFileDialog, QMessageBox,
    QTabWidget, QWidget, QCheckBox
)
from PyQt6.QtCore import Qt
from pathlib import Path

from ltwin_manager.utils.config_manager import get_config_manager
from ltwin_manager.utils.network_manager import get_network_manager


class VMConfigDialog(QDialog):
    """虚拟机配置对话框"""
    
    def __init__(self, vm_name=None, parent=None):
        super().__init__(parent)
        self.vm_name = vm_name
        self.config_manager = get_config_manager()
        self.network_manager = get_network_manager()
        
        self.setWindowTitle("虚拟机配置" if vm_name else "创建新虚拟机")
        self.resize(700, 600)
        
        self.init_ui()
        if vm_name:
            self.load_vm_config()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 基本配置标签页
        basic_tab = self.create_basic_config_tab()
        tab_widget.addTab(basic_tab, "基本配置")
        
        # 高级配置标签页
        advanced_tab = self.create_advanced_config_tab()
        tab_widget.addTab(advanced_tab, "高级配置")
        
        layout.addWidget(tab_widget)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def create_basic_config_tab(self):
        """创建基本配置标签页"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # 虚拟机名称
        self.name_edit = QLineEdit()
        if self.vm_name:
            self.name_edit.setText(self.vm_name)
            self.name_edit.setReadOnly(True)  # 编辑时不允许更改名称
        else:
            self.name_edit.setPlaceholderText("请输入虚拟机名称")
        layout.addRow("虚拟机名称:", self.name_edit)
        
        # CPU核心数
        self.cpu_spinbox = QSpinBox()
        self.cpu_spinbox.setRange(1, 16)
        self.cpu_spinbox.setValue(self.config_manager.get_global_config("default_vm_cpu_cores") or 2)
        layout.addRow("CPU核心数:", self.cpu_spinbox)
        
        # 内存大小
        self.memory_spinbox = QSpinBox()
        self.memory_spinbox.setRange(512, 65536)
        self.memory_spinbox.setSingleStep(512)
        self.memory_spinbox.setValue(self.config_manager.get_global_config("default_vm_memory_mb") or 2048)
        self.memory_spinbox.setSuffix(" MB")
        layout.addRow("内存大小:", self.memory_spinbox)
        
        # 磁盘大小
        self.disk_size_spinbox = QSpinBox()
        self.disk_size_spinbox.setRange(10, 1000)
        self.disk_size_spinbox.setValue(self.config_manager.get_global_config("default_vm_disk_size_gb") or 20)
        self.disk_size_spinbox.setSuffix(" GB")
        layout.addRow("磁盘大小:", self.disk_size_spinbox)
        
        # 磁盘文件路径
        disk_layout = QHBoxLayout()
        self.disk_path_edit = QLineEdit()
        self.disk_path_edit.setPlaceholderText("虚拟磁盘文件路径")
        disk_browse_btn = QPushButton("浏览...")
        disk_browse_btn.clicked.connect(self.browse_disk_path)
        disk_layout.addWidget(self.disk_path_edit)
        disk_layout.addWidget(disk_browse_btn)
        layout.addRow("磁盘文件:", disk_layout)
        
        # ISO镜像路径
        iso_layout = QHBoxLayout()
        self.iso_path_edit = QLineEdit()
        self.iso_path_edit.setPlaceholderText("ISO镜像文件路径（可选）")
        iso_browse_btn = QPushButton("浏览...")
        iso_browse_btn.clicked.connect(self.browse_iso_path)
        iso_layout.addWidget(self.iso_path_edit)
        iso_layout.addWidget(iso_browse_btn)
        layout.addRow("ISO镜像:", iso_layout)
        
        return widget
    
    def create_advanced_config_tab(self):
        """创建高级配置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 网络配置组
        network_group = QGroupBox("网络配置")
        network_layout = QFormLayout(network_group)
        
        self.network_combo = QComboBox()
        available_modes = self.network_manager.get_available_network_modes()
        self.network_combo.addItems(available_modes)
        network_layout.addRow("网络模式:", self.network_combo)
        
        self.mac_edit = QLineEdit()
        self.mac_edit.setPlaceholderText("留空以自动生成MAC地址")
        network_layout.addRow("MAC地址:", self.mac_edit)
        
        layout.addWidget(network_group)
        
        # 显示配置组
        display_group = QGroupBox("显示配置")
        display_layout = QFormLayout(display_group)
        
        self.vga_combo = QComboBox()
        self.vga_combo.addItems(["std", "cirrus", "vmware", "qxl", "virtio"])
        self.vga_combo.setCurrentText("virtio")
        display_layout.addRow("显卡类型:", self.vga_combo)
        
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["自动", "1024x768", "1280x720", "1920x1080"])
        display_layout.addRow("分辨率:", self.resolution_combo)
        
        layout.addWidget(display_group)
        
        # 其他选项组
        other_group = QGroupBox("其他选项")
        other_layout = QGridLayout(other_group)
        
        self.enable_usb_checkbox = QCheckBox("启用USB支持")
        self.enable_usb_checkbox.setChecked(True)
        other_layout.addWidget(self.enable_usb_checkbox, 0, 0)
        
        self.enable_audio_checkbox = QCheckBox("启用音频支持")
        other_layout.addWidget(self.enable_audio_checkbox, 0, 1)
        
        self.boot_from_cd_checkbox = QCheckBox("从CD-ROM启动")
        other_layout.addWidget(self.boot_from_cd_checkbox, 1, 0)
        
        self.enable_efi_checkbox = QCheckBox("启用EFI支持")
        other_layout.addWidget(self.enable_efi_checkbox, 1, 1)
        
        layout.addWidget(other_group)
        
        return widget
    
    def browse_disk_path(self):
        """浏览磁盘文件路径"""
        start_path = self.config_manager.get_default_vm_storage_path()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "选择虚拟磁盘文件",
            str(start_path / f"{self.name_edit.text() or 'new_vm'}.qcow2"),
            "QCOW2文件 (*.qcow2);;IMG文件 (*.img);;所有文件 (*)"
        )
        if file_path:
            self.disk_path_edit.setText(file_path)
    
    def browse_iso_path(self):
        """浏览ISO文件路径"""
        start_path = self.config_manager.get_default_iso_storage_path()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择ISO镜像文件",
            str(start_path),
            "ISO文件 (*.iso);;所有文件 (*)"
        )
        if file_path:
            self.iso_path_edit.setText(file_path)
    
    def load_vm_config(self):
        """加载现有虚拟机配置"""
        config = self.config_manager.get_vm_config(self.vm_name)
        if not config:
            return
        
        # 基本配置
        self.name_edit.setText(config.get('name', ''))
        self.cpu_spinbox.setValue(config.get('cpu_cores', 2))
        self.memory_spinbox.setValue(config.get('memory_mb', 2048))
        
        disk_size = self.calculate_disk_size(config.get('disk_path', ''))
        if disk_size > 0:
            self.disk_size_spinbox.setValue(disk_size)
        self.disk_path_edit.setText(config.get('disk_path', ''))
        
        self.iso_path_edit.setText(config.get('iso_path', ''))
    
    def calculate_disk_size(self, disk_path):
        """计算磁盘文件大小（GB）"""
        try:
            if disk_path and Path(disk_path).exists():
                size_bytes = Path(disk_path).stat().st_size
                size_gb = size_bytes / (1024**3)
                return int(size_gb)
        except:
            pass
        return 20  # 默认20GB
    
    def validate_inputs(self):
        """验证输入"""
        vm_name = self.name_edit.text().strip()
        if not vm_name:
            QMessageBox.warning(self, "输入错误", "请输入虚拟机名称")
            return False
        
        if not self.vm_name and self.config_manager.vm_exists(vm_name):
            QMessageBox.warning(self, "名称冲突", f"虚拟机 '{vm_name}' 已存在")
            return False
        
        disk_path = self.disk_path_edit.text().strip()
        if not disk_path:
            QMessageBox.warning(self, "输入错误", "请选择虚拟磁盘文件路径")
            return False
        
        iso_path = self.iso_path_edit.text().strip()
        if iso_path and not Path(iso_path).exists():
            reply = QMessageBox.question(
                self,
                "文件不存在",
                f"ISO文件 '{iso_path}' 不存在，是否继续？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return False
        
        return True
    
    def accept(self):
        """确认保存配置"""
        if not self.validate_inputs():
            return
        
        # 创建配置字典
        config = {
            'name': self.name_edit.text().strip(),
            'cpu_cores': self.cpu_spinbox.value(),
            'memory_mb': self.memory_spinbox.value(),
            'disk_path': self.disk_path_edit.text().strip(),
            'iso_path': self.iso_path_edit.text().strip(),
            'vnc_port': self.config_manager.get_next_vnc_port(),
            'network_mode': self.network_combo.currentText(),
            'vga_type': self.vga_combo.currentText(),
            'status': 'stopped' if self.vm_name else 'configured'  # 如果是编辑现有VM，保持原状态
        }
        
        # 保存配置
        vm_name = self.name_edit.text().strip()
        if self.config_manager.set_vm_config(vm_name, config):
            QMessageBox.information(self, "成功", f"虚拟机配置已{'更新' if self.vm_name else '创建'}")
            super().accept()
        else:
            QMessageBox.critical(self, "错误", "保存配置失败")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    dialog = VMConfigDialog()
    dialog.show()
    sys.exit(app.exec())