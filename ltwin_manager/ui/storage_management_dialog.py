# -*- coding: utf-8 -*-
"""
存储管理对话框
用于管理虚拟机存储空间
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QTabWidget, QWidget, QGroupBox, QPushButton,
    QLabel, QProgressBar, QTreeWidget, QTreeWidgetItem,
    QHeaderView, QMessageBox, QSpinBox, QLineEdit
)
from PyQt6.QtCore import Qt
from datetime import datetime


class StorageManagementDialog(QDialog):
    """存储管理对话框"""
    
    def __init__(self, storage_manager, config_manager, parent=None):
        super().__init__(parent)
        self.storage_manager = storage_manager
        self.config_manager = config_manager
        
        self.setWindowTitle("存储管理")
        self.resize(800, 600)
        
        self.init_ui()
        self.load_storage_info()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 存储概览标签页
        overview_tab = self.create_overview_tab()
        tab_widget.addTab(overview_tab, "存储概览")
        
        # 虚拟机存储标签页
        vm_storage_tab = self.create_vm_storage_tab()
        tab_widget.addTab(vm_storage_tab, "虚拟机存储")
        
        # 快照存储标签页
        snapshot_storage_tab = self.create_snapshot_storage_tab()
        tab_widget.addTab(snapshot_storage_tab, "快照存储")
        
        # 磁盘操作标签页
        disk_ops_tab = self.create_disk_operations_tab()
        tab_widget.addTab(disk_ops_tab, "磁盘操作")
        
        layout.addWidget(tab_widget)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self.load_storage_info)
        
        self.cleanup_btn = QPushButton("清理旧文件")
        self.cleanup_btn.clicked.connect(self.cleanup_old_files)
        
        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.cleanup_btn)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
    
    def create_overview_tab(self):
        """创建存储概览标签页"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # 系统磁盘信息
        sys_disk_group = QGroupBox("系统磁盘信息")
        sys_disk_layout = QFormLayout(sys_disk_group)
        
        self.sys_disk_info = QLabel("加载中...")
        sys_disk_layout.addRow("系统磁盘:", self.sys_disk_info)
        
        layout.addWidget(sys_disk_group)
        
        # LTWin存储信息
        ltwin_storage_group = QGroupBox("LTWin存储信息")
        ltwin_storage_layout = QFormLayout(ltwin_storage_group)
        
        self.ltwin_storage_info = QLabel("加载中...")
        ltwin_storage_layout.addRow("LTWin存储:", self.ltwin_storage_info)
        
        # 存储使用进度条
        self.storage_usage_bar = QProgressBar()
        self.storage_usage_value = QLabel("0%")
        storage_usage_layout = QHBoxLayout()
        storage_usage_layout.addWidget(self.storage_usage_bar)
        storage_usage_layout.addWidget(self.storage_usage_value)
        ltwin_storage_layout.addRow("存储使用率:", storage_usage_layout)
        
        layout.addWidget(ltwin_storage_group)
        
        # 统计信息
        stats_group = QGroupBox("统计信息")
        stats_layout = QFormLayout(stats_group)
        
        self.total_vms_label = QLabel("0")
        stats_layout.addRow("虚拟机总数:", self.total_vms_label)
        
        self.total_usage_label = QLabel("0 GB")
        stats_layout.addRow("总使用空间:", self.total_usage_label)
        
        self.largest_vm_label = QLabel("N/A")
        stats_layout.addRow("最大虚拟机:", self.largest_vm_label)
        
        layout.addWidget(stats_group)
        
        return widget
    
    def create_vm_storage_tab(self):
        """创建虚拟机存储标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 虚拟机存储列表
        self.vm_storage_tree = QTreeWidget()
        self.vm_storage_tree.setHeaderLabels(["虚拟机", "大小", "路径"])
        header = self.vm_storage_tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(QLabel("虚拟机存储列表:"))
        layout.addWidget(self.vm_storage_tree)
        
        # 操作按钮
        vm_ops_layout = QHBoxLayout()
        
        self.expand_all_btn = QPushButton("展开全部")
        self.expand_all_btn.clicked.connect(self.vm_storage_tree.expandAll)
        
        self.collapse_all_btn = QPushButton("折叠全部")
        self.collapse_all_btn.clicked.connect(self.vm_storage_tree.collapseAll)
        
        vm_ops_layout.addWidget(self.expand_all_btn)
        vm_ops_layout.addWidget(self.collapse_all_btn)
        vm_ops_layout.addStretch()
        
        layout.addLayout(vm_ops_layout)
        
        return widget
    
    def create_snapshot_storage_tab(self):
        """创建快照存储标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 快照存储列表
        self.snapshot_storage_tree = QTreeWidget()
        self.snapshot_storage_tree.setHeaderLabels(["快照", "大小", "创建时间", "路径"])
        header = self.snapshot_storage_tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(QLabel("快照存储列表:"))
        layout.addWidget(self.snapshot_storage_tree)
        
        return widget
    
    def create_disk_operations_tab(self):
        """创建磁盘操作标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 磁盘创建组
        create_group = QGroupBox("创建虚拟磁盘")
        create_layout = QFormLayout(create_group)
        
        self.disk_path_edit = QLineEdit()
        self.disk_path_edit.setPlaceholderText("输入磁盘文件路径")
        create_layout.addRow("磁盘路径:", self.disk_path_edit)
        
        self.disk_size_spin = QSpinBox()
        self.disk_size_spin.setRange(1, 1000)
        self.disk_size_spin.setValue(20)
        self.disk_size_spin.setSuffix(" GB")
        create_layout.addRow("磁盘大小:", self.disk_size_spin)
        
        self.create_disk_btn = QPushButton("创建磁盘")
        self.create_disk_btn.clicked.connect(self.create_virtual_disk)
        create_layout.addRow("", self.create_disk_btn)
        
        layout.addWidget(create_group)
        
        # 磁盘调整组
        resize_group = QGroupBox("调整磁盘大小")
        resize_layout = QFormLayout(resize_group)
        
        self.resize_path_edit = QLineEdit()
        self.resize_path_edit.setPlaceholderText("输入现有磁盘文件路径")
        resize_layout.addRow("磁盘路径:", self.resize_path_edit)
        
        self.resize_size_spin = QSpinBox()
        self.resize_size_spin.setRange(1, 10000)
        self.resize_size_spin.setValue(30)
        self.resize_size_spin.setSuffix(" GB")
        resize_layout.addRow("新大小:", self.resize_size_spin)
        
        self.resize_disk_btn = QPushButton("调整大小")
        self.resize_disk_btn.clicked.connect(self.resize_virtual_disk)
        resize_layout.addRow("", self.resize_disk_btn)
        
        layout.addWidget(resize_group)
        
        return widget
    
    def load_storage_info(self):
        """加载存储信息"""
        # 加载系统磁盘信息
        sys_disks = self.storage_manager.get_system_disks()
        if sys_disks:
            disk_info = sys_disks[0]  # 显示第一个磁盘信息
            self.sys_disk_info.setText(
                f"{disk_info.path} - 总共: {disk_info.total_size / (1024**3):.2f} GB, "
                f"已用: {disk_info.used_size / (1024**3):.2f} GB, "
                f"可用: {disk_info.free_size / (1024**3):.2f} GB"
            )
        
        # 加载LTWin存储信息
        ltwin_disk_info = self.storage_manager.get_ltwin_storage_usage()
        self.ltwin_storage_info.setText(
            f"{ltwin_disk_info.path} - 总共: {ltwin_disk_info.total_size / (1024**3):.2f} GB, "
            f"已用: {ltwin_disk_info.used_size / (1024**3):.2f} GB"
        )
        
        # 更新存储使用进度条
        usage_percent = ltwin_disk_info.usage_percent
        self.storage_usage_bar.setValue(int(usage_percent))
        self.storage_usage_value.setText(f"{usage_percent:.1f}%")
        
        # 加载统计信息
        stats = self.storage_manager.get_disk_statistics()
        self.total_vms_label.setText(str(stats['total_vms']))
        self.total_usage_label.setText(f"{stats['total_disk_usage'] / (1024**3):.2f} GB")
        self.largest_vm_label.setText(f"{stats['largest_vm']} ({stats['largest_vm_size'] / (1024**3):.2f} GB)")
        
        # 加载虚拟机存储列表
        self.load_vm_storage_list()
        
        # 加载快照存储列表
        self.load_snapshot_storage_list()
    
    def load_vm_storage_list(self):
        """加载虚拟机存储列表"""
        self.vm_storage_tree.clear()
        
        vm_stats = self.storage_manager.get_disk_statistics()
        
        for vm_name, size in vm_stats['vm_count_by_size']:
            size_gb = size / (1024**3)
            item = QTreeWidgetItem([vm_name, f"{size_gb:.2f} GB", str(self.storage_manager.base_path / vm_name)])
            self.vm_storage_tree.addTopLevelItem(item)
    
    def load_snapshot_storage_list(self):
        """加载快照存储列表"""
        # 这里可以加载快照信息，暂时显示占位符
        self.snapshot_storage_tree.clear()
        
        # 添加示例数据
        snapshot_item = QTreeWidgetItem(["示例快照", "2.5 GB", "2023-01-01 12:00", "/path/to/snapshot"])
        self.snapshot_storage_tree.addTopLevelItem(snapshot_item)
    
    def create_virtual_disk(self):
        """创建虚拟磁盘"""
        disk_path = self.disk_path_edit.text().strip()
        size_gb = self.disk_size_spin.value()
        
        if not disk_path:
            QMessageBox.warning(self, "输入错误", "请输入磁盘文件路径")
            return
        
        success = self.storage_manager.create_disk_image(disk_path, size_gb)
        if success:
            QMessageBox.information(self, "成功", f"虚拟磁盘 {disk_path} 创建成功")
            self.disk_path_edit.clear()
        else:
            QMessageBox.critical(self, "错误", f"创建虚拟磁盘失败: {disk_path}")
    
    def resize_virtual_disk(self):
        """调整虚拟磁盘大小"""
        disk_path = self.resize_path_edit.text().strip()
        new_size_gb = self.resize_size_spin.value()
        
        if not disk_path:
            QMessageBox.warning(self, "输入错误", "请输入磁盘文件路径")
            return
        
        success = self.storage_manager.resize_disk_image(disk_path, new_size_gb)
        if success:
            QMessageBox.information(self, "成功", f"虚拟磁盘 {disk_path} 大小已调整为 {new_size_gb} GB")
            self.resize_path_edit.clear()
        else:
            QMessageBox.critical(self, "错误", f"调整虚拟磁盘大小失败: {disk_path}")
    
    def cleanup_old_files(self):
        """清理旧文件"""
        reply = QMessageBox.question(
            self,
            "确认清理",
            "确定要清理30天前的旧文件吗？此操作不可撤销！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            cleaned_count = self.storage_manager.cleanup_old_snapshots(30)
            QMessageBox.information(self, "清理完成", f"已清理 {cleaned_count} 个旧快照文件")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    from ltwin_manager.utils.storage_manager import get_storage_manager
    from ltwin_manager.utils.config_manager import get_config_manager
    
    app = QApplication(sys.argv)
    config_manager = get_config_manager()
    storage_manager = get_storage_manager(config_manager)
    dialog = StorageManagementDialog(storage_manager, config_manager)
    dialog.show()
    sys.exit(app.exec())