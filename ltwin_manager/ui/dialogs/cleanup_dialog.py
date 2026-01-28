"""
环境清理对话框
"""

import sys
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QGroupBox, 
                             QFormLayout, QApplication, QWidget, QCheckBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont


class CleanupThread(QThread):
    """清理操作线程"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool)
    
    def __init__(self, operations, home_path):
        super().__init__()
        self.operations = operations
        self.home_path = home_path
        
    def run(self):
        """执行清理操作"""
        from ..utils.cleanup_tool import CleanupTool
        
        try:
            if 'user_dirs' in self.operations:
                self.progress.emit('正在清除用户目录...')
                success = CleanupTool.clear_user_directories(self.home_path)
                if success:
                    self.progress.emit('用户目录清除完成')
                else:
                    self.progress.emit('用户目录清除失败')
            
            if 'apps' in self.operations:
                self.progress.emit('正在清除应用程序...')
                success = CleanupTool.clear_application_dirs(self.home_path)
                if success:
                    self.progress.emit('应用程序清除完成')
                else:
                    self.progress.emit('应用程序清除失败')
                    
            if 'flutter' in self.operations:
                self.progress.emit('正在清除Flutter相关文件...')
                success = CleanupTool.clear_flutter_dirs(self.home_path)
                if success:
                    self.progress.emit('Flutter相关文件清除完成')
                else:
                    self.progress.emit('Flutter相关文件清除失败')
                    
            if 'snapshots' in self.operations:
                self.progress.emit('正在重置虚拟机快照...')
                # TODO: 传入配置管理器
                success = CleanupTool.reset_vm_snapshots(None)
                if success:
                    self.progress.emit('虚拟机快照重置完成')
                else:
                    self.progress.emit('虚拟机快照重置失败')
                    
            if 'configs' in self.operations:
                self.progress.emit('正在重置配置文件...')
                # TODO: 传入配置管理器
                success = CleanupTool.reset_configuration_files(None)
                if success:
                    self.progress.emit('配置文件重置完成')
                else:
                    self.progress.emit('配置文件重置失败')
            
            self.progress.emit('所有清理操作已完成')
            self.finished.emit(True)
            
        except Exception as e:
            self.progress.emit(f'清理过程中发生错误: {str(e)}')
            self.finished.emit(False)


class CleanupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('环境清理')
        self.setModal(True)
        self.resize(500, 400)
        
        self.cleanup_thread = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel('清理系统环境')
        title_label.setFont(QFont('Microsoft YaHei', 12, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # 清理选项
        cleanup_group = QGroupBox('选择要清理的项目')
        cleanup_layout = QVBoxLayout()
        
        self.clear_user_dirs = QCheckBox('清除用户目录(~/.*)')
        self.clear_user_dirs.setChecked(False)
        cleanup_layout.addWidget(self.clear_user_dirs)
        
        self.clear_apps = QCheckBox('清除应用程序(myapp)')
        self.clear_apps.setChecked(False)
        cleanup_layout.addWidget(self.clear_apps)
        
        self.clear_flutter = QCheckBox('清除Flutter相关文件')
        self.clear_flutter.setChecked(False)
        cleanup_layout.addWidget(self.clear_flutter)
        
        self.reset_vm_snapshots = QCheckBox('重置虚拟机快照')
        self.reset_vm_snapshots.setChecked(False)
        cleanup_layout.addWidget(self.reset_vm_snapshots)
        
        self.reset_configs = QCheckBox('重置配置文件')
        self.reset_configs.setChecked(False)
        cleanup_layout.addWidget(self.reset_configs)
        
        cleanup_group.setLayout(cleanup_layout)
        layout.addWidget(cleanup_group)
        
        # 路径配置（如果适用）
        path_group = QGroupBox('路径配置')
        path_layout = QFormLayout()
        
        self.user_home_path = QLineEdit(os.path.expanduser('~'))
        path_layout.addRow('用户主目录:', self.user_home_path)
        
        path_group.setLayout(path_layout)
        layout.addWidget(path_group)
        
        # 确认信息
        confirm_label = QLabel('警告: 此操作不可逆，请确认要执行的清理项目！')
        confirm_label.setStyleSheet('color: red; font-weight: bold')
        layout.addWidget(confirm_label)
        
        # 状态显示
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        self.cleanup_btn = QPushButton('执行清理')
        self.cleanup_btn.clicked.connect(self.perform_cleanup)
        
        self.cancel_btn = QPushButton('取消')
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.cleanup_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def perform_cleanup(self):
        """执行清理操作"""
        operations = []
        if self.clear_user_dirs.isChecked():
            operations.append('user_dirs')
        if self.clear_apps.isChecked():
            operations.append('apps')
        if self.clear_flutter.isChecked():
            operations.append('flutter')
        if self.reset_vm_snapshots.isChecked():
            operations.append('snapshots')
        if self.reset_configs.isChecked():
            operations.append('configs')
        
        if not operations:
            self.status_text.append('请至少选择一个要清理的项目')
            return
        
        # 确认操作
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self, 
            '确认清理操作', 
            f'即将执行清理操作: {", ".join(operations)}\n此操作不可逆，是否继续？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # 创建并启动清理线程
        self.cleanup_btn.setEnabled(False)
        self.cleanup_thread = CleanupThread(operations, self.user_home_path.text())
        self.cleanup_thread.progress.connect(self.status_text.append)
        self.cleanup_thread.finished.connect(self.on_cleanup_finished)
        self.cleanup_thread.start()
    
    def on_cleanup_finished(self, success):
        """清理完成回调"""
        if success:
            self.status_text.append('所有清理操作已完成')
        else:
            self.status_text.append('部分清理操作可能失败，请检查上面的日志')
        self.cleanup_btn.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = CleanupDialog()
    dialog.exec()
    sys.exit(app.exec())