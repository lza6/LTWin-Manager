# -*- coding: utf-8 -*-
"""
系统检测对话框
用于检测系统环境并修复缺失的组件
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QTextEdit,
    QPushButton, QLabel, QProgressBar, QGroupBox, QScrollArea,
    QWidget, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from ltwin_manager.utils.system_checker import SystemChecker
from ltwin_manager.ui.performance_report_dialog import PerformanceReportDialog


class SystemCheckWorker(QThread):
    """系统检查工作线程"""
    
    progress_signal = pyqtSignal(str, int)  # (状态消息, 进度百分比)
    result_signal = pyqtSignal(dict)  # 检查结果
    
    def __init__(self):
        super().__init__()
        self.checker = SystemChecker()
    
    def run(self):
        """执行系统检查"""
        # 连接进度信号
        self.checker.check_progress.connect(self.progress_signal.emit)
        # 执行检查
        result = self.checker.run_comprehensive_check()
        # 发送结果
        self.result_signal.emit(result)


class RepairWorker(QThread):
    """修复工作线程"""
    
    progress_signal = pyqtSignal(str, int)  # (状态消息, 进度百分比)
    complete_signal = pyqtSignal(bool)  # 修复完成状态
    
    def __init__(self, checker: SystemChecker):
        super().__init__()
        self.checker = checker
    
    def run(self):
        """执行修复"""
        # 连接进度和完成信号
        self.checker.repair_progress.connect(self.progress_signal.emit)
        self.checker.repair_complete.connect(self.complete_signal.emit)
        # 执行修复
        success = self.checker.repair_missing_components()


class SystemCheckDialog(QDialog):
    """系统检测对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checker = SystemChecker()
        self.check_worker = None
        self.repair_worker = None
        
        self.setWindowTitle("系统检测和修复工具")
        self.resize(700, 500)
        
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("系统检测和修复工具")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # 说明文字
        info_label = QLabel("此工具将检测您的系统环境并帮助您修复缺失的组件")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        layout.addWidget(self.create_separator())
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # 状态标签
        self.status_label = QLabel("准备就绪")
        layout.addWidget(self.status_label)
        
        # 结果显示区域
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMaximumHeight(200)
        layout.addWidget(self.result_text)
        
        # 详细信息区域（滚动区域）
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # 系统信息组
        self.system_info_group = QGroupBox("系统信息")
        system_layout = QGridLayout()
        self.system_info_labels = {}
        for i, key in enumerate(['操作系统', '系统版本', '架构', '处理器', 'Python版本', '总内存', '可用内存', '可用磁盘空间']):
            label = QLabel(f"{key}:")
            value_label = QLabel("-")
            value_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            system_layout.addWidget(label, i, 0)
            system_layout.addWidget(value_label, i, 1)
            self.system_info_labels[key] = value_label
        self.system_info_group.setLayout(system_layout)
        scroll_layout.addWidget(self.system_info_group)
        
        # 依赖状态组
        self.dependencies_group = QGroupBox("依赖状态")
        deps_layout = QGridLayout()
        self.dependency_labels = {}
        for i, dep in enumerate(['Python', 'pip', 'PyQt6', 'psutil', 'requests', 'SQLAlchemy', 'paramiko', 'QEMU', 'qemu-img']):
            label = QLabel(f"{dep}:")
            status_label = QLabel("-")
            status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            deps_layout.addWidget(label, i, 0)
            deps_layout.addWidget(status_label, i, 1)
            self.dependency_labels[dep] = status_label
        self.dependencies_group.setLayout(deps_layout)
        scroll_layout.addWidget(self.dependencies_group)
        
        # 缺失组件组
        self.missing_group = QGroupBox("缺失的组件")
        missing_layout = QVBoxLayout()
        self.missing_text = QTextEdit()
        self.missing_text.setMaximumHeight(100)
        self.missing_text.setReadOnly(True)
        missing_layout.addWidget(self.missing_text)
        self.missing_group.setLayout(missing_layout)
        scroll_layout.addWidget(self.missing_group)
        
        # 添加一些间距
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.check_button = QPushButton("开始检测")
        self.check_button.clicked.connect(self.start_check)
        
        self.repair_button = QPushButton("一键修复")
        self.repair_button.clicked.connect(self.start_repair)
        self.repair_button.setEnabled(False)
        
        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.check_button)
        button_layout.addWidget(self.repair_button)
        
        self.performance_report_button = QPushButton("性能报告")
        self.performance_report_button.clicked.connect(self.open_performance_report)
        button_layout.addWidget(self.performance_report_button)
        
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
    
    def create_separator(self):
        """创建分隔线"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        return separator
    
    def setup_connections(self):
        """设置信号连接"""
        pass
    
    def start_check(self):
        """开始系统检查"""
        self.check_button.setEnabled(False)
        self.repair_button.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # 创建并启动检查工作线程
        self.check_worker = SystemCheckWorker()
        self.check_worker.progress_signal.connect(self.update_progress)
        self.check_worker.result_signal.connect(self.display_results)
        self.check_worker.finished.connect(self.check_finished)
        
        self.check_worker.start()
    
    def update_progress(self, status: str, percent: int):
        """更新进度"""
        self.status_label.setText(status)
        self.progress_bar.setValue(percent)
    
    def display_results(self, result: dict):
        """显示检查结果"""
        self.result_text.clear()
        
        if result.get('error'):
            self.result_text.setHtml(f'<font color="red">检测出错: {result["error"]}</font>')
            return
        
        # 显示系统信息
        sys_info = result.get('system_info', {})
        self.system_info_labels['操作系统'].setText(sys_info.get('os', '未知'))
        self.system_info_labels['系统版本'].setText(sys_info.get('os_version', '未知'))
        self.system_info_labels['架构'].setText(sys_info.get('architecture', '未知'))
        self.system_info_labels['处理器'].setText(sys_info.get('processor', '未知'))
        self.system_info_labels['Python版本'].setText(sys_info.get('python_version', '未知'))
        self.system_info_labels['总内存'].setText(f"{sys_info.get('total_memory_gb', '未知')} GB")
        self.system_info_labels['可用内存'].setText(f"{sys_info.get('available_memory_gb', '未知')} GB")
        self.system_info_labels['可用磁盘空间'].setText(f"{sys_info.get('disk_space_gb', '未知')} GB")
        
        # 显示依赖状态
        deps = result.get('dependencies', {})
        dep_mapping = {
            'python': 'Python',
            'pip': 'pip',
            'pyqt6': 'PyQt6',
            'psutil': 'psutil',
            'requests': 'requests',
            'sqlalchemy': 'SQLAlchemy',
            'paramiko': 'paramiko',
            'qemu': 'QEMU',
            'qemu_img': 'qemu-img'
        }
        
        for key, display_name in dep_mapping.items():
            status = "✓ 已安装" if deps.get(key, False) else "✗ 未安装"
            color = "green" if deps.get(key, False) else "red"
            self.dependency_labels[display_name].setText(f'<font color="{color}">{status}</font>')
        
        # 显示缺失组件
        missing = result.get('missing_components', [])
        if missing:
            missing_text = "\\n".join(missing)
            self.missing_text.setPlainText(missing_text)
            self.result_text.append(f"⚠️ 检测到 {len(missing)} 个缺失的组件:\\n{missing_text}")
        else:
            self.missing_text.setPlainText("无缺失组件")
            self.result_text.append("✅ 所有必需组件均已安装！")
        
        # 显示虚拟化支持
        virtualization_ok = result.get('virtualization_supported', False)
        virtualization_status = "✓ 支持" if virtualization_ok else "⚠ 不支持或未知"
        virtualization_color = "green" if virtualization_ok else "orange"
        self.result_text.append(f"\\n虚拟化支持: <font color='{virtualization_color}'>{virtualization_status}</font>")
        
        # 更新按钮状态
        self.repair_button.setEnabled(len(missing) > 0)
    
    def check_finished(self):
        """检查完成后的处理"""
        self.check_button.setEnabled(True)
    
    def start_repair(self):
        """开始修复"""
        reply = QMessageBox.question(
            self,
            "确认修复",
            "此操作将尝试修复所有缺失的组件，可能需要一些时间。是否继续？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        self.check_button.setEnabled(False)
        self.repair_button.setEnabled(False)
        
        # 创建并启动修复工作线程
        self.repair_worker = RepairWorker(self.checker)
        self.repair_worker.progress_signal.connect(self.update_progress)
        self.repair_worker.complete_signal.connect(self.repair_completed)
        self.repair_worker.finished.connect(self.repair_finished)
        
        self.repair_worker.start()
    
    def repair_completed(self, success: bool):
        """修复完成"""
        if success:
            QMessageBox.information(self, "修复完成", "组件修复完成！请重新检测系统状态。")
        else:
            QMessageBox.warning(self, "修复完成", "部分组件未能成功修复，请手动安装缺失的组件。")
    
    def repair_finished(self):
        """修复线程结束"""
        self.check_button.setEnabled(True)
        self.repair_button.setEnabled(True)
        self.progress_bar.setValue(100)
        self.status_label.setText("修复完成，点击检测按钮重新检查")
    
    def open_performance_report(self):
        """打开性能报告"""
        try:
            dialog = PerformanceReportDialog(self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法打开性能报告对话框:\n{str(e)}")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    dialog = SystemCheckDialog()
    dialog.show()
    sys.exit(app.exec())