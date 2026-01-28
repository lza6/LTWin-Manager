# -*- coding: utf-8 -*-
"""
快照管理对话框
用于管理虚拟机快照的创建、恢复、删除等操作
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QTextEdit, QPushButton, QLabel, 
    QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QMessageBox, QSplitter, QWidget
)
from PyQt6.QtCore import Qt
from datetime import datetime


class SnapshotDialog(QDialog):
    """快照管理对话框"""
    
    def __init__(self, vm_name, vm_controller, parent=None):
        super().__init__(parent)
        self.vm_name = vm_name
        self.vm_controller = vm_controller
        
        self.setWindowTitle(f"{vm_name} - 快照管理")
        self.resize(800, 600)
        
        self.init_ui()
        self.load_snapshots()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 快照操作组
        operation_group = QGroupBox("快照操作")
        operation_layout = QHBoxLayout(operation_group)
        
        self.snapshot_name_edit = QLineEdit()
        self.snapshot_name_edit.setPlaceholderText("输入快照名称")
        operation_layout.addWidget(QLabel("快照名称:"))
        operation_layout.addWidget(self.snapshot_name_edit)
        
        self.create_snapshot_btn = QPushButton("创建快照")
        self.create_snapshot_btn.clicked.connect(self.create_snapshot)
        operation_layout.addWidget(self.create_snapshot_btn)
        
        operation_layout.addStretch()
        
        layout.addWidget(operation_group)
        
        # 快照描述
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("快照描述:"))
        self.snapshot_desc_edit = QTextEdit()
        self.snapshot_desc_edit.setMaximumHeight(60)
        desc_layout.addWidget(self.snapshot_desc_edit)
        
        layout.addLayout(desc_layout)
        
        # 快照列表
        self.snapshots_table = QTableWidget()
        self.snapshots_table.setColumnCount(5)
        self.snapshots_table.setHorizontalHeaderLabels(["ID", "名称", "描述", "创建时间", "操作"])
        header = self.snapshots_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.snapshots_table.setAlternatingRowColors(True)
        self.snapshots_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(QLabel("快照列表:"))
        layout.addWidget(self.snapshots_table)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self.load_snapshots)
        
        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
    
    def load_snapshots(self):
        """加载快照列表"""
        snapshots = self.vm_controller.list_vm_snapshots(self.vm_name)
        
        self.snapshots_table.setRowCount(len(snapshots))
        
        for row, snapshot in enumerate(snapshots):
            self.snapshots_table.setItem(row, 0, QTableWidgetItem(snapshot['id']))
            self.snapshots_table.setItem(row, 1, QTableWidgetItem(snapshot['name']))
            self.snapshots_table.setItem(row, 2, QTableWidgetItem(snapshot['description']))
            self.snapshots_table.setItem(row, 3, QTableWidgetItem(snapshot['created_at']))
            
            # 操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(2, 2, 2, 2)
            
            restore_btn = QPushButton("恢复")
            restore_btn.clicked.connect(lambda _, s=snapshot['id']: self.restore_snapshot(s))
            restore_btn.setStyleSheet("QPushButton { color: blue; }")
            
            delete_btn = QPushButton("删除")
            delete_btn.clicked.connect(lambda _, s=snapshot['id']: self.delete_snapshot(s))
            delete_btn.setStyleSheet("QPushButton { color: red; }")
            
            btn_layout.addWidget(restore_btn)
            btn_layout.addWidget(delete_btn)
            btn_layout.addStretch()
            
            self.snapshots_table.setCellWidget(row, 4, btn_widget)
    
    def create_snapshot(self):
        """创建快照"""
        snapshot_name = self.snapshot_name_edit.text().strip()
        if not snapshot_name:
            QMessageBox.warning(self, "输入错误", "请输入快照名称")
            return
        
        description = self.snapshot_desc_edit.toPlainText().strip()
        
        try:
            success = self.vm_controller.create_vm_snapshot(self.vm_name, snapshot_name, description)
            if success:
                QMessageBox.information(self, "成功", "快照创建成功")
                self.load_snapshots()
                self.snapshot_name_edit.clear()
                self.snapshot_desc_edit.clear()
            else:
                QMessageBox.critical(self, "错误", "快照创建失败")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建快照时发生错误:\\n{str(e)}")
    
    def restore_snapshot(self, snapshot_id):
        """恢复快照"""
        reply = QMessageBox.question(
            self, 
            "确认恢复", 
            f"确定要恢复快照 '{snapshot_id}' 吗？\\n此操作将覆盖当前虚拟机状态！", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.vm_controller.restore_vm_snapshot(self.vm_name, snapshot_id)
                if success:
                    QMessageBox.information(self, "成功", "快照恢复成功")
                else:
                    QMessageBox.critical(self, "错误", "快照恢复失败")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"恢复快照时发生错误:\\n{str(e)}")
    
    def delete_snapshot(self, snapshot_id):
        """删除快照"""
        reply = QMessageBox.question(
            self, 
            "确认删除", 
            f"确定要删除快照 '{snapshot_id}' 吗？\\n此操作不可撤销！", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.vm_controller.delete_vm_snapshot(self.vm_name, snapshot_id)
                if success:
                    QMessageBox.information(self, "成功", "快照删除成功")
                    self.load_snapshots()
                else:
                    QMessageBox.critical(self, "错误", "快照删除失败")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除快照时发生错误:\\n{str(e)}")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    # dialog = SnapshotDialog("test_vm", None)
    # dialog.show()
    sys.exit(app.exec())