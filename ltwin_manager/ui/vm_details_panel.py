# -*- coding: utf-8 -*-
"""
虚拟机详情面板
用于显示虚拟机的详细信息和状态
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QGroupBox, QLabel, QProgressBar, QPushButton,
    QTextEdit, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt
from datetime import datetime
from pathlib import Path
import psutil


class VMDetailsPanel(QWidget):
    """虚拟机详情面板"""
    
    def __init__(self, vm_controller, parent=None):
        super().__init__(parent)
        self.vm_controller = vm_controller
        
        self.vm_name = None
        self.vm_config = None
        
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 虚拟机基本信息组
        info_group = QGroupBox("虚拟机信息")
        info_layout = QFormLayout(info_group)
        
        self.vm_name_label = QLabel("-")
        info_layout.addRow("虚拟机名称:", self.vm_name_label)
        
        self.vm_status_label = QLabel("-")
        info_layout.addRow("状态:", self.vm_status_label)
        
        self.vm_created_label = QLabel("-")
        info_layout.addRow("创建时间:", self.vm_created_label)
        
        self.vm_last_started_label = QLabel("-")
        info_layout.addRow("最后启动:", self.vm_last_started_label)
        
        layout.addWidget(info_group)
        
        # 硬件配置组
        hardware_group = QGroupBox("硬件配置")
        hardware_layout = QFormLayout(hardware_group)
        
        self.cpu_label = QLabel("-")
        hardware_layout.addRow("CPU核心数:", self.cpu_label)
        
        self.memory_label = QLabel("-")
        hardware_layout.addRow("内存大小:", self.memory_label)
        
        self.disk_label = QLabel("-")
        hardware_layout.addRow("磁盘路径:", self.disk_label)
        
        self.network_label = QLabel("-")
        hardware_layout.addRow("网络模式:", self.network_label)
        
        self.mac_label = QLabel("-")
        hardware_layout.addRow("MAC地址:", self.mac_label)
        
        layout.addWidget(hardware_group)
        
        # 运行状态组
        status_group = QGroupBox("运行状态")
        status_layout = QGridLayout(status_group)
        
        # CPU使用率
        cpu_label = QLabel("CPU使用率:")
        self.cpu_progress = QProgressBar()
        self.cpu_value_label = QLabel("0%")
        status_layout.addWidget(cpu_label, 0, 0)
        status_layout.addWidget(self.cpu_progress, 0, 1)
        status_layout.addWidget(self.cpu_value_label, 0, 2)
        
        # 内存使用率
        mem_label = QLabel("内存使用率:")
        self.mem_progress = QProgressBar()
        self.mem_value_label = QLabel("0%")
        status_layout.addWidget(mem_label, 1, 0)
        status_layout.addWidget(self.mem_progress, 1, 1)
        status_layout.addWidget(self.mem_value_label, 1, 2)
        
        # 磁盘使用率
        disk_label = QLabel("磁盘使用率:")
        self.disk_progress = QProgressBar()
        self.disk_value_label = QLabel("0%")
        status_layout.addWidget(disk_label, 2, 0)
        status_layout.addWidget(self.disk_progress, 2, 1)
        status_layout.addWidget(self.disk_value_label, 2, 2)
        
        # 网络使用率
        net_label = QLabel("网络使用率:")
        self.net_progress = QProgressBar()
        self.net_value_label = QLabel("0%")
        status_layout.addWidget(net_label, 3, 0)
        status_layout.addWidget(self.net_progress, 3, 1)
        status_layout.addWidget(self.net_value_label, 3, 2)
        
        status_layout.setColumnStretch(1, 1)
        
        layout.addWidget(status_group)
        
        # 操作按钮组
        action_group = QGroupBox("操作")
        action_layout = QHBoxLayout(action_group)
        
        self.start_btn = QPushButton("启动")
        self.start_btn.clicked.connect(self.start_vm)
        
        self.stop_btn = QPushButton("停止")
        self.stop_btn.clicked.connect(self.stop_vm)
        
        self.pause_btn = QPushButton("暂停")
        self.pause_btn.clicked.connect(self.pause_vm)
        
        self.edit_btn = QPushButton("编辑配置")
        self.edit_btn.clicked.connect(self.edit_vm)
        
        action_layout.addWidget(self.start_btn)
        action_layout.addWidget(self.stop_btn)
        action_layout.addWidget(self.pause_btn)
        action_layout.addWidget(self.edit_btn)
        action_layout.addStretch()
        
        layout.addWidget(action_group)
        
        # 存储信息组
        storage_group = QGroupBox("存储信息")
        storage_layout = QFormLayout(storage_group)
        
        self.disk_size_label = QLabel("-")
        storage_layout.addRow("磁盘大小:", self.disk_size_label)
        
        self.disk_usage_label = QLabel("-")
        storage_layout.addRow("磁盘使用:", self.disk_usage_label)
        
        self.disk_free_label = QLabel("-")
        storage_layout.addRow("可用空间:", self.disk_free_label)
        
        layout.addWidget(storage_group)
        
        # 日志输出区域
        log_group = QGroupBox("日志输出")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setReadOnly(True)
        
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        # 添加弹性空间
        layout.addStretch()
    
    def load_vm(self, vm_name):
        """加载虚拟机信息"""
        self.vm_name = vm_name
        self.vm_config = self.vm_controller.config_manager.get_vm_config(vm_name)
        
        if self.vm_config:
            self.vm_name_label.setText(self.vm_config.get('name', '-'))
            self.vm_status_label.setText(self.vm_config.get('status', '-'))
            self.vm_created_label.setText(self.vm_config.get('created_at', '-'))
            self.vm_last_started_label.setText(self.vm_config.get('last_started', '-'))
            
            self.cpu_label.setText(f"{self.vm_config.get('cpu_cores', '?')} 核心")
            self.memory_label.setText(f"{self.vm_config.get('memory_mb', '?')} MB")
            self.disk_label.setText(self.vm_config.get('disk_path', '-'))
            self.network_label.setText(self.vm_config.get('network_mode', '-'))
            self.mac_label.setText(self.vm_config.get('mac_address', '-'))
            
            # 更新存储信息
            self.update_storage_info()
            
            # 更新按钮状态
            self.update_buttons()
        else:
            self.log_text.append(f"错误: 无法找到虚拟机 {vm_name} 的配置")
    
    def update_buttons(self):
        """更新按钮状态"""
        if not self.vm_config:
            return
        
        status = self.vm_config.get('status', 'unknown')
        is_running = status == 'running'
        
        self.start_btn.setEnabled(not is_running)
        self.stop_btn.setEnabled(is_running)
        self.pause_btn.setEnabled(is_running)
    
    def update_storage_info(self):
        """更新存储信息"""
        if not self.vm_config:
            return
        
        disk_path = self.vm_config.get('disk_path', '')
        if disk_path and Path(disk_path).exists():
            try:
                disk_stat = Path(disk_path).stat()
                disk_size = disk_stat.st_size
                disk_size_gb = disk_size / (1024**3)
                
                # 获取所在分区的可用空间
                disk_usage = psutil.disk_usage(Path(disk_path).parent)
                free_space_gb = disk_usage.free / (1024**3)
                
                self.disk_size_label.setText(f"{disk_size_gb:.2f} GB")
                self.disk_free_label.setText(f"{free_space_gb:.2f} GB")
                
                # 计算使用率
                partition_usage = psutil.disk_usage(Path(disk_path).parent)
                usage_percent = ((partition_usage.total - partition_usage.free) / partition_usage.total) * 100
                self.disk_usage_label.setText(f"{usage_percent:.1f}%")
            except Exception as e:
                self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 获取磁盘信息失败: {str(e)}")
        else:
            self.disk_size_label.setText("文件不存在")
            self.disk_usage_label.setText("-")
            self.disk_free_label.setText("-")
    
    def start_vm(self):
        """启动虚拟机"""
        if not self.vm_name or not self.vm_config:
            return
        
        try:
            success = self.vm_controller.start_vm_with_config(self.vm_config)
            if success:
                self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 虚拟机 {self.vm_name} 启动成功")
                self.vm_config['status'] = 'running'
                self.vm_controller.config_manager.set_vm_config(self.vm_name, self.vm_config)
                self.update_buttons()
            else:
                self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 虚拟机 {self.vm_name} 启动失败")
        except Exception as e:
            self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 启动虚拟机失败: {str(e)}")
    
    def stop_vm(self):
        """停止虚拟机"""
        if not self.vm_name:
            return
        
        try:
            success = self.vm_controller.stop_vm(self.vm_name)
            if success:
                self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 虚拟机 {self.vm_name} 停止成功")
                self.vm_config = self.vm_controller.config_manager.get_vm_config(self.vm_name)
                if self.vm_config:
                    self.vm_config['status'] = 'stopped'
                    self.vm_controller.config_manager.set_vm_config(self.vm_name, self.vm_config)
                    self.update_buttons()
            else:
                self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 虚拟机 {self.vm_name} 停止失败")
        except Exception as e:
            self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 停止虚拟机失败: {str(e)}")
    
    def pause_vm(self):
        """暂停虚拟机"""
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 暂停功能将在后续版本中实现")
    
    def edit_vm(self):
        """编辑虚拟机"""
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 编辑功能将在后续版本中实现")
    
    def update_vm_status(self, system_info):
        """更新虚拟机状态显示"""
        if isinstance(system_info, dict):
            # 更新CPU使用率
            cpu_percent = system_info.get('cpu_percent', 0)
            self.cpu_progress.setValue(int(cpu_percent))
            self.cpu_value_label.setText(f"{cpu_percent}%")
            
            # 更新内存使用率
            mem_info = system_info.get('memory', {})
            mem_percent = mem_info.get('percent', 0)
            self.mem_progress.setValue(int(mem_percent))
            self.mem_value_label.setText(f"{mem_percent}%")
            
            # 更新磁盘使用率
            disk_info = system_info.get('disk', {})
            disk_percent = disk_info.get('percent', 0)
            self.disk_progress.setValue(int(disk_percent))
            self.disk_value_label.setText(f"{disk_percent}%")
            
            # 更新网络使用率（这里只是一个示意值）
            self.net_progress.setValue(0)
            self.net_value_label.setText("0%")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    from ltwin_manager.controllers.vm_controller import VMController
    from ltwin_manager.utils.config_manager import get_config_manager
    
    app = QApplication(sys.argv)
    config_manager = get_config_manager()
    vm_controller = VMController(config_manager)
    panel = VMDetailsPanel(vm_controller)
    panel.show()
    sys.exit(app.exec())