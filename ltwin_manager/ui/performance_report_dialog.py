# -*- coding: utf-8 -*-
"""
性能报告对话框
显示系统和虚拟机性能分析报告
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QTabWidget, QWidget, QFormLayout, QLabel, QProgressBar,
    QGroupBox, QListWidget
)
from PyQt6.QtCore import Qt
from ltwin_manager.utils.performance_optimizer import get_performance_optimizer
from ltwin_manager.utils.system_monitor import SystemMonitor


class PerformanceReportDialog(QDialog):
    """性能报告对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.performance_optimizer = get_performance_optimizer()
        self.system_monitor = SystemMonitor()
        
        self.setWindowTitle("系统性能报告")
        self.resize(800, 600)
        
        self.init_ui()
        self.generate_report()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 系统概览标签页
        overview_tab = self.create_overview_tab()
        tab_widget.addTab(overview_tab, "系统概览")
        
        # 性能建议标签页
        recommendations_tab = self.create_recommendations_tab()
        tab_widget.addTab(recommendations_tab, "性能建议")
        
        # 详细信息标签页
        details_tab = self.create_details_tab()
        tab_widget.addTab(details_tab, "详细信息")
        
        layout.addWidget(tab_widget)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def create_overview_tab(self):
        """创建系统概览标签页"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # 获取系统信息
        system_info = self.system_monitor.get_detailed_system_info()
        
        # CPU信息
        cpu_group = QGroupBox("CPU信息")
        cpu_layout = QFormLayout(cpu_group)
        cpu_layout.addRow("架构:", QLabel(system_info.get('system_machine', 'Unknown')))
        cpu_layout.addRow("处理器:", QLabel(system_info.get('system_processor', 'Unknown')))
        cpu_layout.addRow("核心数:", QLabel(str(system_info.get('process_count', 'Unknown'))))
        
        layout.addWidget(cpu_group)
        
        # 内存信息
        memory_group = QGroupBox("内存信息")
        memory_layout = QFormLayout(memory_group)
        memory_info = system_info.get('memory_info', {})
        total_mem = memory_info.get('total', 0) / (1024**3) if 'total' in memory_info else 0
        available_mem = memory_info.get('available', 0) / (1024**3) if 'available' in memory_info else 0
        memory_layout.addRow("总内存:", QLabel(f"{total_mem:.2f} GB"))
        memory_layout.addRow("可用内存:", QLabel(f"{available_mem:.2f} GB"))
        memory_layout.addRow("使用率:", QLabel(f"{memory_info.get('percent', 0)}%"))
        
        # 内存使用进度条
        mem_progress = QProgressBar()
        mem_progress.setValue(int(memory_info.get('percent', 0)))
        memory_layout.addRow("内存使用:", mem_progress)
        
        layout.addWidget(memory_group)
        
        # 磁盘信息
        disk_group = QGroupBox("磁盘信息")
        disk_layout = QFormLayout(disk_group)
        disk_info = system_info.get('disk_io', {})
        disk_layout.addRow("总空间:", QLabel(f"{disk_info.get('read_mb', 0) + disk_info.get('write_mb', 0):.2f} GB"))
        
        layout.addWidget(disk_group)
        
        return widget
    
    def create_recommendations_tab(self):
        """创建性能建议标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 系统性能建议
        sys_rec_group = QGroupBox("系统性能建议")
        sys_rec_layout = QVBoxLayout(sys_rec_group)
        
        sys_recommendations = self.performance_optimizer.get_system_performance_tips()
        sys_rec_list = QListWidget()
        for tip in sys_recommendations:
            sys_rec_list.addItem(tip)
        
        sys_rec_layout.addWidget(sys_rec_list)
        layout.addWidget(sys_rec_group)
        
        # 虚拟机性能建议
        vm_rec_group = QGroupBox("虚拟机配置建议")
        vm_rec_layout = QVBoxLayout(vm_rec_group)
        
        vm_rec_list = QListWidget()
        # 这里可以传入虚拟机配置来获取建议
        vm_recommendations = ["请在虚拟机详情中查看针对特定虚拟机的性能建议"]
        for rec in vm_recommendations:
            vm_rec_list.addItem(rec)
        
        vm_rec_layout.addWidget(vm_rec_list)
        layout.addWidget(vm_rec_group)
        
        return widget
    
    def create_details_tab(self):
        """创建详细信息标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 详细系统信息文本框
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        
        layout.addWidget(QLabel("详细系统信息:"))
        layout.addWidget(self.details_text)
        
        return widget
    
    def generate_report(self):
        """生成性能报告"""
        try:
            # 获取详细系统信息
            system_info = self.system_monitor.get_detailed_system_info()
            
            # 构建报告内容
            report_lines = [
                "LTWin Manager 系统性能报告",
                "=" * 40,
                "",
                "系统信息:",
                f"  平台: {system_info.get('system_platform', 'Unknown')}",
                f"  机器: {system_info.get('system_machine', 'Unknown')}",
                f"  处理器: {system_info.get('system_processor', 'Unknown')}",
                f"  节点: {system_info.get('system_node', 'Unknown')}",
                f"  启动时间: {system_info.get('boot_time', 'Unknown')}",
                "",
                "CPU信息:",
                f"  逻辑核心数: {system_info.get('process_count', 'Unknown')}",
                "",
                "内存信息:",
                f"  总内存: {system_info.get('memory_info', {}).get('total', 0) / (1024**3):.2f} GB",
                f"  可用内存: {system_info.get('memory_info', {}).get('available', 0) / (1024**3):.2f} GB",
                f"  使用率: {system_info.get('memory_info', {}).get('percent', 0)}%",
                "",
                "交换内存:",
                f"  总量: {system_info.get('swap_info', {}).get('total', 0) / (1024**3):.2f} GB",
                f"  使用量: {system_info.get('swap_info', {}).get('used', 0) / (1024**3):.2f} GB",
                f"  使用率: {system_info.get('swap_info', {}).get('percent', 0)}%",
                "",
                "网络信息:",
                f"  发送: {system_info.get('network', {}).get('sent_mb', 0):.2f} MB",
                f"  接收: {system_info.get('network', {}).get('recv_mb', 0):.2f} MB",
                "",
                "磁盘IO信息:",
                f"  读取: {system_info.get('disk_io', {}).get('read_mb', 0):.2f} MB",
                f"  写入: {system_info.get('disk_io', {}).get('write_mb', 0):.2f} MB",
                "",
                "推荐设置:",
                f"  推荐CPU核心: {self.performance_optimizer.recommended_settings['recommended_cpu']}",
                f"  推荐内存: {self.performance_optimizer.recommended_settings['recommended_memory_mb']} MB",
                f"  推荐磁盘大小: {self.performance_optimizer.recommended_settings['recommended_disk_size_gb']} GB",
                f"  KVM支持: {'是' if self.performance_optimizer.is_kvm_supported else '否'}",
                "",
                "性能优化建议:",
            ]
            
            # 添加性能建议
            sys_tips = self.performance_optimizer.get_system_performance_tips()
            for tip in sys_tips:
                report_lines.append(f"  • {tip}")
            
            report_text = "\n".join(report_lines)
            self.details_text.setPlainText(report_text)
            
        except Exception as e:
            error_text = f"生成性能报告时发生错误: {str(e)}"
            self.details_text.setPlainText(error_text)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    dialog = PerformanceReportDialog()
    dialog.show()
    sys.exit(app.exec())