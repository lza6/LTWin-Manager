# -*- coding: utf-8 -*-
"""
设置对话框
用于配置LTWin Manager的各种设置
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QTabWidget, QWidget, QGroupBox, QCheckBox,
    QPushButton, QLabel, QComboBox, QSpinBox,
    QDoubleSpinBox, QLineEdit, QTextEdit, QSlider
)
from PyQt6.QtCore import Qt


class SettingsDialog(QDialog):
    """设置对话框"""
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        
        self.setWindowTitle("LTWin Manager - 设置")
        self.resize(600, 500)
        
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 通用设置标签页
        general_tab = self.create_general_tab()
        tab_widget.addTab(general_tab, "常规")
        
        # 外观设置标签页
        appearance_tab = self.create_appearance_tab()
        tab_widget.addTab(appearance_tab, "外观")
        
        # 性能设置标签页
        performance_tab = self.create_performance_tab()
        tab_widget.addTab(performance_tab, "性能")
        
        # 高级设置标签页
        advanced_tab = self.create_advanced_tab()
        tab_widget.addTab(advanced_tab, "高级")
        
        layout.addWidget(tab_widget)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.apply_button = QPushButton("应用")
        self.apply_button.clicked.connect(self.apply_settings)
        
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def create_general_tab(self):
        """创建常规设置标签页"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # 语言设置
        self.language_combo = QComboBox()
        self.language_combo.addItems(["简体中文", "English"])
        layout.addRow("界面语言:", self.language_combo)
        
        # 自动检查更新
        self.auto_update_check = QCheckBox("启动时自动检查更新")
        layout.addWidget(self.auto_update_check)
        
        # 显示系统托盘图标
        self.tray_icon_check = QCheckBox("显示系统托盘图标")
        layout.addWidget(self.tray_icon_check)
        
        # 虚拟机存储路径
        path_layout = QHBoxLayout()
        self.vm_storage_edit = QLineEdit()
        self.vm_storage_btn = QPushButton("浏览...")
        path_layout.addWidget(self.vm_storage_edit)
        path_layout.addWidget(self.vm_storage_btn)
        layout.addRow("虚拟机存储路径:", path_layout)
        
        # ISO存储路径
        iso_path_layout = QHBoxLayout()
        self.iso_storage_edit = QLineEdit()
        self.iso_storage_btn = QPushButton("浏览...")
        iso_path_layout.addWidget(self.iso_storage_edit)
        iso_path_layout.addWidget(self.iso_storage_btn)
        layout.addRow("ISO存储路径:", iso_path_layout)
        
        return widget
    
    def create_appearance_tab(self):
        """创建外观设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 主题设置组
        theme_group = QGroupBox("主题设置")
        theme_layout = QFormLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["暗色", "亮色", "蓝色"])
        theme_layout.addRow("界面主题:", self.theme_combo)
        
        layout.addWidget(theme_group)
        
        # 字体设置组
        font_group = QGroupBox("字体设置")
        font_layout = QFormLayout(font_group)
        
        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems(["默认", "微软雅黑", "宋体", "Arial", "Times New Roman"])
        font_layout.addRow("字体家族:", self.font_family_combo)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        font_layout.addRow("字体大小:", self.font_size_spin)
        
        layout.addWidget(font_group)
        
        # 界面效果组
        effect_group = QGroupBox("界面效果")
        effect_layout = QVBoxLayout(effect_group)
        
        self.animation_check = QCheckBox("启用动画效果")
        effect_layout.addWidget(self.animation_check)
        
        self.transparency_check = QCheckBox("启用透明效果")
        effect_layout.addWidget(self.transparency_check)
        
        layout.addWidget(effect_group)
        
        return widget
    
    def create_performance_tab(self):
        """创建性能设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 虚拟机性能组
        vm_perf_group = QGroupBox("虚拟机性能")
        vm_perf_layout = QFormLayout(vm_perf_group)
        
        self.default_cpu_spin = QSpinBox()
        self.default_cpu_spin.setRange(1, 16)
        vm_perf_layout.addRow("默认CPU核心数:", self.default_cpu_spin)
        
        self.default_memory_spin = QSpinBox()
        self.default_memory_spin.setRange(512, 65536)
        self.default_memory_spin.setSuffix(" MB")
        vm_perf_layout.addRow("默认内存大小:", self.default_memory_spin)
        
        self.default_disk_spin = QSpinBox()
        self.default_disk_spin.setRange(10, 1000)
        self.default_disk_spin.setSuffix(" GB")
        vm_perf_layout.addRow("默认磁盘大小:", self.default_disk_spin)
        
        layout.addWidget(vm_perf_group)
        
        # 系统性能组
        sys_perf_group = QGroupBox("系统性能")
        sys_perf_layout = QVBoxLayout(sys_perf_group)
        
        self.auto_optimize_check = QCheckBox("自动优化虚拟机性能")
        sys_perf_layout.addWidget(self.auto_optimize_check)
        
        self.kvm_check = QCheckBox("启用KVM硬件加速（如可用）")
        sys_perf_layout.addWidget(self.kvm_check)
        
        max_vms_layout = QHBoxLayout()
        max_vms_layout.addWidget(QLabel("最大并发虚拟机数量:"))
        self.max_vms_spin = QSpinBox()
        self.max_vms_spin.setRange(1, 10)
        max_vms_layout.addWidget(self.max_vms_spin)
        max_vms_layout.addStretch()
        sys_perf_layout.addLayout(max_vms_layout)
        
        layout.addWidget(sys_perf_group)
        
        return widget
    
    def create_advanced_tab(self):
        """创建高级设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 高级选项组
        advanced_group = QGroupBox("高级选项")
        advanced_layout = QVBoxLayout(advanced_group)
        
        self.enable_snapshots_check = QCheckBox("启用快照功能")
        advanced_layout.addWidget(self.enable_snapshots_check)
        
        snapshot_path_layout = QHBoxLayout()
        snapshot_path_layout.addWidget(QLabel("快照存储路径:"))
        self.snapshot_path_edit = QLineEdit()
        self.snapshot_path_btn = QPushButton("浏览...")
        snapshot_path_layout.addWidget(self.snapshot_path_edit)
        snapshot_path_layout.addWidget(self.snapshot_path_btn)
        advanced_layout.addLayout(snapshot_path_layout)
        
        self.enable_cloning_check = QCheckBox("启用克隆功能")
        advanced_layout.addWidget(self.enable_cloning_check)
        
        layout.addWidget(advanced_group)
        
        # 自定义参数组
        custom_group = QGroupBox("自定义参数")
        custom_layout = QVBoxLayout(custom_group)
        
        self.custom_args_edit = QTextEdit()
        self.custom_args_edit.setMaximumHeight(100)
        custom_layout.addWidget(QLabel("自定义QEMU参数:"))
        custom_layout.addWidget(self.custom_args_edit)
        
        layout.addWidget(custom_group)
        
        return widget
    
    def load_settings(self):
        """加载当前设置"""
        # 通用设置
        language = self.config_manager.get_global_config("language") or "zh-CN"
        self.language_combo.setCurrentText("简体中文" if language == "zh-CN" else "English")
        
        auto_update = self.config_manager.get_global_config("auto_check_updates")
        self.auto_update_check.setChecked(auto_update if auto_update is not None else True)
        
        show_tray = self.config_manager.get_global_config("show_tray_icon")
        self.tray_icon_check.setChecked(show_tray if show_tray is not None else True)
        
        vm_storage = self.config_manager.get_global_config("vm_storage_path")
        self.vm_storage_edit.setText(vm_storage or str(self.config_manager.get_default_vm_storage_path()))
        
        iso_storage = self.config_manager.get_global_config("iso_storage_path")
        self.iso_storage_edit.setText(iso_storage or str(self.config_manager.get_default_iso_storage_path()))
        
        # 外观设置
        theme = self.config_manager.get_global_config("theme") or "dark"
        theme_map = {"dark": "暗色", "light": "亮色", "blue": "蓝色"}
        self.theme_combo.setCurrentText(theme_map.get(theme, "暗色"))
        
        # 性能设置
        default_cpu = self.config_manager.get_global_config("default_vm_cpu_cores")
        self.default_cpu_spin.setValue(default_cpu or 2)
        
        default_memory = self.config_manager.get_global_config("default_vm_memory_mb")
        self.default_memory_spin.setValue(default_memory or 2048)
        
        default_disk = self.config_manager.get_global_config("default_vm_disk_size_gb")
        self.default_disk_spin.setValue(default_disk or 20)
        
        auto_optimize = self.config_manager.get_global_config("auto_optimize_vm")
        self.auto_optimize_check.setChecked(auto_optimize if auto_optimize is not None else True)
        
        check_kvm = self.config_manager.get_global_config("check_kvm_support")
        self.kvm_check.setChecked(check_kvm if check_kvm is not None else True)
        
        max_vms = self.config_manager.get_global_config("max_concurrent_vms")
        self.max_vms_spin.setValue(max_vms or 5)
        
        # 高级设置
        enable_snapshots = self.config_manager.get_global_config("enable_snapshots")
        self.enable_snapshots_check.setChecked(enable_snapshots if enable_snapshots is not None else True)
        
        snapshot_location = self.config_manager.get_global_config("snapshot_location")
        self.snapshot_path_edit.setText(snapshot_location or str(self.config_manager.get_default_vm_storage_path() / "Snapshots"))
        
        # 这里可以添加更多设置的加载
    
    def apply_settings(self):
        """应用设置"""
        # 保存通用设置
        language_map = {"简体中文": "zh-CN", "English": "en-US"}
        self.config_manager.set_global_config("language", language_map.get(self.language_combo.currentText(), "zh-CN"))
        self.config_manager.set_global_config("auto_check_updates", self.auto_update_check.isChecked())
        self.config_manager.set_global_config("show_tray_icon", self.tray_icon_check.isChecked())
        self.config_manager.set_global_config("vm_storage_path", self.vm_storage_edit.text())
        self.config_manager.set_global_config("iso_storage_path", self.iso_storage_edit.text())
        
        # 保存外观设置
        theme_map = {"暗色": "dark", "亮色": "light", "蓝色": "blue"}
        self.config_manager.set_global_config("theme", theme_map.get(self.theme_combo.currentText(), "dark"))
        
        # 保存性能设置
        self.config_manager.set_global_config("default_vm_cpu_cores", self.default_cpu_spin.value())
        self.config_manager.set_global_config("default_vm_memory_mb", self.default_memory_spin.value())
        self.config_manager.set_global_config("default_vm_disk_size_gb", self.default_disk_spin.value())
        self.config_manager.set_global_config("auto_optimize_vm", self.auto_optimize_check.isChecked())
        self.config_manager.set_global_config("check_kvm_support", self.kvm_check.isChecked())
        self.config_manager.set_global_config("max_concurrent_vms", self.max_vms_spin.value())
        
        # 保存高级设置
        self.config_manager.set_global_config("enable_snapshots", self.enable_snapshots_check.isChecked())
        self.config_manager.set_global_config("snapshot_location", self.snapshot_path_edit.text())
        
        # 通知父窗口更新UI
        if hasattr(self.parent(), 'on_settings_changed'):
            self.parent().on_settings_changed()
    
    def accept(self):
        """确认并应用设置"""
        self.apply_settings()
        super().accept()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    from ltwin_manager.utils.config_manager import get_config_manager
    
    app = QApplication(sys.argv)
    config_manager = get_config_manager()
    dialog = SettingsDialog(config_manager)
    dialog.show()
    sys.exit(app.exec())