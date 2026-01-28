# -*- coding: utf-8 -*-
"""
LTWin Manager 主窗口
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeWidget, QTreeWidgetItem, QStackedWidget, QMenuBar,
    QStatusBar, QMessageBox, QToolBar, QLabel, QProgressBar,
    QSystemTrayIcon, QMenu, QInputDialog, QLineEdit
)
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QKeySequence

from ltwin_manager.controllers.vm_controller import VMController
from ltwin_manager.utils.system_monitor import SystemMonitor
from ltwin_manager.utils.config_manager import get_config_manager
from ltwin_manager.ui.vm_config_dialog import VMConfigDialog
from ltwin_manager.ui.system_check_dialog import SystemCheckDialog
from ltwin_manager.ui.snapshot_dialog import SnapshotDialog
from ltwin_manager.ui.performance_report_dialog import PerformanceReportDialog
from ltwin_manager.ui.settings_dialog import SettingsDialog
from ltwin_manager.ui.vm_details_panel import VMDetailsPanel
from ltwin_manager.ui.storage_management_dialog import StorageManagementDialog
from ltwin_manager.ui.security_audit_dialog import SecurityAuditDialog
from ltwin_manager.ui.security_config_dialog import SecurityConfigDialog
from ltwin_manager.utils.clone_manager import get_clone_manager
from ltwin_manager.utils.theme_manager import get_theme_manager
from ltwin_manager.utils.storage_manager import get_storage_manager
from ltwin_manager.utils.permission_manager import get_permission_manager

from ltwin_manager.ui.dialogs.download_images_dialog import DownloadImagesDialog
from ltwin_manager.ui.dialogs.vm_start_options_dialog import VMStartOptionsDialog
from ltwin_manager.ui.dialogs.chrome_manager_dialog import ChromeManagerDialog
from ltwin_manager.ui.dialogs.cleanup_dialog import CleanupDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = get_config_manager()
        self.vm_controller = VMController(self.config_manager)
        self.clone_manager = get_clone_manager(self.config_manager)
        self.storage_manager = get_storage_manager(self.config_manager)
        self.permission_manager = get_permission_manager(self.config_manager)
        self.theme_manager = get_theme_manager(self.config_manager)
        self.system_monitor = SystemMonitor()
        
        self.init_ui()
        self.setup_connections()
        self.load_data()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("LTWin Manager - 虚拟机管理软件")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(QSize(1000, 600))
        
        # 设置窗口图标
        # icon_path = "ltwin_manager/resources/icons/app_icon.png"
        # if os.path.exists(icon_path):
        #     self.setWindowIcon(QIcon(icon_path))
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建中央部件
        self.setup_central_widget()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 创建系统托盘（可选）
        self.create_system_tray()
        
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')
        
        new_vm_action = QAction('新建虚拟机(&N)', self)
        new_vm_action.setShortcut(QKeySequence.StandardKey.New)
        new_vm_action.triggered.connect(self.new_vm)
        file_menu.addAction(new_vm_action)
        
        file_menu.addSeparator()
        
        settings_action = QAction('设置(&S)', self)
        settings_action.setShortcut(QKeySequence.StandardKey.Preferences)
        settings_action.triggered.connect(self.open_settings)
        file_menu.addAction(settings_action)
        
        theme_menu = file_menu.addMenu('主题(&T)')
        
        dark_theme_action = QAction('暗色主题', self)
        dark_theme_action.triggered.connect(lambda: self.change_theme('dark'))
        theme_menu.addAction(dark_theme_action)
        
        light_theme_action = QAction('亮色主题', self)
        light_theme_action.triggered.connect(lambda: self.change_theme('light'))
        theme_menu.addAction(light_theme_action)
        
        warm_white_theme_action = QAction('暖白色主题', self)
        warm_white_theme_action.triggered.connect(lambda: self.change_theme('warm_white'))
        theme_menu.addAction(warm_white_theme_action)
        
        blue_theme_action = QAction('蓝色主题', self)
        blue_theme_action.triggered.connect(lambda: self.change_theme('blue'))
        theme_menu.addAction(blue_theme_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('退出(&X)', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 管理菜单
        manager_menu = menubar.addMenu('管理(&M)')
        
        refresh_action = QAction('刷新(&R)', self)
        refresh_action.setShortcut(QKeySequence.StandardKey.Refresh)
        refresh_action.triggered.connect(self.refresh_data)
        manager_menu.addAction(refresh_action)
        
        snapshot_action = QAction('快照管理(&S)', self)
        snapshot_action.triggered.connect(self.open_snapshot_manager)
        manager_menu.addAction(snapshot_action)
        
        clone_action = QAction('克隆虚拟机(&C)', self)
        clone_action.triggered.connect(self.clone_selected_vm)
        manager_menu.addAction(clone_action)
        
        download_action = QAction('下载镜像(&D)', self)
        download_action.triggered.connect(self.download_images)
        manager_menu.addAction(download_action)
        
        chrome_manage_action = QAction('Chrome管理(&C)', self)
        chrome_manage_action.triggered.connect(self.manage_chrome_installation)
        manager_menu.addAction(chrome_manage_action)
        
        cleanup_action = QAction('环境清理(&E)', self)
        cleanup_action.triggered.connect(self.cleanup_environment)
        manager_menu.addAction(cleanup_action)
        
        backup_action = QAction('备份虚拟机(&B)', self)
        backup_action.triggered.connect(self.backup_vm)
        manager_menu.addAction(backup_action)
        
        # 配置菜单
        config_menu = menubar.addMenu('配置(&C)')
        
        manage_vms_action = QAction('管理虚拟机配置(&V)', self)
        manage_vms_action.triggered.connect(self.manage_vm_configs)
        config_menu.addAction(manage_vms_action)
        
        manage_images_action = QAction('管理镜像文件(&I)', self)
        manage_images_action.triggered.connect(self.manage_image_configs)
        config_menu.addAction(manage_images_action)
        
        # 工具菜单
        tools_menu = menubar.addMenu('工具(&T)')
        
        system_check_action = QAction('系统检测和修复(&C)', self)
        system_check_action.triggered.connect(self.open_system_check)
        tools_menu.addAction(system_check_action)
        
        storage_mgmt_action = QAction('存储管理(&M)', self)
        storage_mgmt_action.triggered.connect(self.open_storage_management)
        tools_menu.addAction(storage_mgmt_action)
        
        performance_report_action = QAction('性能报告(&P)', self)
        performance_report_action.triggered.connect(self.open_performance_report)
        tools_menu.addAction(performance_report_action)
        
        # 安全菜单
        security_menu = menubar.addMenu('安全(&S)')
        
        security_config_action = QAction('安全配置(&C)', self)
        security_config_action.triggered.connect(self.open_security_config)
        security_menu.addAction(security_config_action)
        
        security_audit_action = QAction('安全审计(&A)', self)
        security_audit_action.triggered.connect(self.open_security_audit)
        security_menu.addAction(security_audit_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')
        
        about_action = QAction('关于(&A)', self)
        about_action.triggered.connect(self.about_dialog)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = self.addToolBar('Main')
        toolbar.setMovable(True)
        
        new_vm_action = QAction('新建虚拟机', self)
        new_vm_action.triggered.connect(self.new_vm)
        toolbar.addAction(new_vm_action)
        
        toolbar.addSeparator()
        
        start_action = QAction('启动', self)
        start_action.triggered.connect(self.start_selected_vm)
        toolbar.addAction(start_action)
        
        stop_action = QAction('停止', self)
        stop_action.triggered.connect(self.stop_selected_vm)
        toolbar.addAction(stop_action)
        
        edit_action = QAction('编辑配置', self)
        edit_action.triggered.connect(self.edit_selected_vm)
        toolbar.addAction(edit_action)
        
        toolbar.addSeparator()
        
        snapshot_action = QAction('快照管理', self)
        snapshot_action.triggered.connect(self.open_snapshot_manager)
        toolbar.addAction(snapshot_action)
        
        clone_action = QAction('克隆虚拟机', self)
        clone_action.triggered.connect(self.clone_selected_vm)
        toolbar.addAction(clone_action)
        
        chrome_manage_action = QAction('Chrome管理', self)
        chrome_manage_action.triggered.connect(self.manage_chrome_installation)
        toolbar.addAction(chrome_manage_action)
        
        cleanup_action = QAction('环境清理', self)
        cleanup_action.triggered.connect(self.cleanup_environment)
        toolbar.addAction(cleanup_action)
        
        storage_mgmt_action = QAction('存储管理', self)
        storage_mgmt_action.triggered.connect(self.open_storage_management)
        toolbar.addAction(storage_mgmt_action)
        
        performance_report_action = QAction('性能报告', self)
        performance_report_action.triggered.connect(self.open_performance_report)
        toolbar.addAction(performance_report_action)
        
        security_config_action = QAction('安全配置', self)
        security_config_action.triggered.connect(self.open_security_config)
        toolbar.addAction(security_config_action)
        
        security_audit_action = QAction('安全审计', self)
        security_audit_action.triggered.connect(self.open_security_audit)
        toolbar.addAction(security_audit_action)
        
        system_check_action = QAction('系统检测', self)
        system_check_action.triggered.connect(self.open_system_check)
        toolbar.addAction(system_check_action)
        
        refresh_action = QAction('刷新', self)
        refresh_action.triggered.connect(self.refresh_data)
        toolbar.addAction(refresh_action)
        
        # 主题切换按钮
        self.theme_cycle_action = QAction('切换主题', self)
        self.theme_cycle_action.triggered.connect(self.cycle_theme)
        toolbar.addAction(self.theme_cycle_action)
        
    def cycle_theme(self):
        """循环切换主题"""
        # 定义主题循环顺序
        themes = ['warm_white', 'light', 'dark', 'blue']
        
        # 获取当前主题
        current_theme = self.config_manager.get_global_config('theme')
        if not current_theme:
            current_theme = 'warm_white'
        
        try:
            # 找到当前主题的索引
            current_index = themes.index(current_theme)
            # 计算下一个主题的索引
            next_index = (current_index + 1) % len(themes)
            next_theme = themes[next_index]
        except ValueError:
            # 如果当前主题不在列表中，使用第一个主题
            next_theme = themes[0]
        
        # 切换到下一个主题
        self.change_theme(next_theme)
        
        # 更新状态栏提示
        theme_names = {
            'warm_white': '暖白色',
            'light': '亮色',
            'dark': '暗色',
            'blue': '蓝色'
        }
        self.statusBar().showMessage(f'已切换到{theme_names.get(next_theme, next_theme)}主题', 2000)
    
    def setup_central_widget(self):
        """设置中央部件"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        
        # 左侧树形视图
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel('资源管理器')
        self.tree_widget.setMaximumWidth(250)
        
        # 右侧内容区域
        self.stacked_widget = QStackedWidget()
        
        # 初始化虚拟机详情页面
        self.vm_details_panel = VMDetailsPanel(self.vm_controller)
        self.stacked_widget.addWidget(self.vm_details_panel)
        
        # 分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.tree_widget)
        splitter.addWidget(self.stacked_widget)
        splitter.setSizes([250, 950])
        
        layout.addWidget(splitter)
        
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 添加系统资源监控标签
        self.cpu_label = QLabel('CPU: 0%')
        self.mem_label = QLabel('内存: 0GB/0GB')
        self.disk_label = QLabel('磁盘: 0GB/0GB')
        
        self.status_bar.addPermanentWidget(self.cpu_label)
        self.status_bar.addPermanentWidget(self.mem_label)
        self.status_bar.addPermanentWidget(self.disk_label)
        
        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # 添加连接状态指示器
        self.connection_label = QLabel('● 已连接')
        self.connection_label.setStyleSheet('color: green;')
        self.status_bar.addPermanentWidget(self.connection_label)
        
    def create_system_tray(self):
        """创建系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        # tray_icon_path = "ltwin_manager/resources/icons/tray_icon.png"
        # if os.path.exists(tray_icon_path):
        #     self.tray_icon.setIcon(QIcon(tray_icon_path))
        # else:
        #     # 使用默认图标
        #     self.tray_icon.setIcon(self.style().standardIcon(
        #         getattr(self.style(), 'SP_ComputerIcon', 44)))
        
        # 创建托盘菜单
        tray_menu = QMenu()
        restore_action = QAction('恢复窗口', self)
        restore_action.triggered.connect(self.showNormal)
        tray_menu.addAction(restore_action)
        
        quit_action = QAction('退出', self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        # self.tray_icon.show()
        
    def setup_connections(self):
        """设置信号连接"""
        self.tree_widget.itemClicked.connect(self.on_tree_item_clicked)
        self.system_monitor.resource_updated.connect(self.update_resource_labels)
        
        # 启动系统监控
        self.system_monitor.start_monitoring()
        
    def load_data(self):
        """加载数据"""
        self.load_vms()
        self.load_images()
        self.load_storage_info()
        
    def load_vms(self):
        """加载虚拟机列表"""
        # 清空现有项
        self.tree_widget.clear()
        
        # 添加根节点
        vms_root = QTreeWidgetItem(self.tree_widget, ['虚拟机'])
        # vms_root.setIcon(0, QIcon('ltwin_manager/resources/icons/vm_folder.png'))
        
        # 加载虚拟机列表
        vms = self.config_manager.list_vms()
        for vm_name in vms:
            vm_config = self.config_manager.get_vm_config(vm_name)
            if vm_config:
                vm_item = QTreeWidgetItem(vms_root, [vm_config.get('name', vm_name)])
                vm_item.setData(0, Qt.ItemDataRole.UserRole, ('vm', vm_name))
                
                # 根据状态设置图标
                status = vm_config.get('status', 'unknown')
                # if status == 'running':
                #     vm_item.setIcon(0, QIcon('ltwin_manager/resources/icons/vm_running.png'))
                # elif status == 'stopped':
                #     vm_item.setIcon(0, QIcon('ltwin_manager/resources/icons/vm_stopped.png'))
                # elif status == 'paused':
                #     vm_item.setIcon(0, QIcon('ltwin_manager/resources/icons/vm_paused.png'))
                # else:
                #     vm_item.setIcon(0, QIcon('ltwin_manager/resources/icons/vm_unknown.png'))
        
        # 展开根节点
        vms_root.setExpanded(True)
        
    def load_images(self):
        """加载镜像列表"""
        # 在虚拟机节点下查找或创建镜像节点
        root_items = self.tree_widget.findItems('虚拟机', Qt.MatchFlag.MatchExactly)
        if root_items:
            images_root = QTreeWidgetItem(root_items[0], ['镜像文件'])
            # images_root.setIcon(0, QIcon('ltwin_manager/resources/icons/image_folder.png'))
            
            images = self.config_manager.list_images()
            for img_name in images:
                img_config = self.config_manager.get_image_config(img_name)
                if img_config:
                    img_item = QTreeWidgetItem(images_root, [img_config.get('name', img_name)])
                    img_item.setData(0, Qt.ItemDataRole.UserRole, ('image', img_config.get('path')))
                    # img_item.setIcon(0, QIcon('ltwin_manager/resources/icons/iso_file.png'))
            
            # 展开镜像节点
            images_root.setExpanded(True)
        
    def load_storage_info(self):
        """加载存储信息"""
        # 在虚拟机节点下查找或创建存储节点
        root_items = self.tree_widget.findItems('虚拟机', Qt.MatchFlag.MatchExactly)
        if root_items:
            storage_root = QTreeWidgetItem(root_items[0], ['存储管理'])
            # storage_root.setIcon(0, QIcon('ltwin_manager/resources/icons/storage_folder.png'))
            
            # 这里可以添加存储信息
            storage_info = [
                {'name': '虚拟机存储', 'path': str(self.config_manager.get_default_vm_storage_path())},
                {'name': '镜像文件存储', 'path': str(self.config_manager.get_default_iso_storage_path())}
            ]
            
            for disk in storage_info:
                disk_item = QTreeWidgetItem(storage_root, [f"{disk['name']} ({disk['path']})"])
                disk_item.setData(0, Qt.ItemDataRole.UserRole, ('storage', disk['path']))
                # disk_item.setIcon(0, QIcon('ltwin_manager/resources/icons/hard_disk.png'))
    
    def on_tree_item_clicked(self, item, column):
        """处理树形视图项点击事件"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data:
            item_type, item_name = data
            if item_type == 'vm':
                self.vm_details_panel.load_vm(item_name)
                self.stacked_widget.setCurrentWidget(self.vm_details_panel)
            elif item_type == 'image':
                self.show_image_details(item_name)
            elif item_type == 'storage':
                self.show_storage_details(item_name)
    
    def show_vm_details(self, vm_name):
        """显示虚拟机详情"""
        # TODO: 实现虚拟机详情显示
        vm_config = self.config_manager.get_vm_config(vm_name)
        if vm_config:
            details = f"虚拟机: {vm_config.get('name', vm_name)}\\n"
            details += f"CPU核心数: {vm_config.get('cpu_cores', '?')}\\n"
            details += f"内存: {vm_config.get('memory_mb', '?')} MB\\n"
            details += f"磁盘: {vm_config.get('disk_path', '?')}\\n"
            details += f"ISO: {vm_config.get('iso_path', '无')}\\n"
            details += f"网络模式: {vm_config.get('network_mode', '用户模式 (User/NAT)')}\\n"
            details += f"MAC地址: {vm_config.get('mac_address', '自动分配')}\\n"
            details += f"状态: {vm_config.get('status', '未知')}\\n"
            details += f"创建时间: {vm_config.get('created_at', '未知')}\\n"
            details += f"最后启动: {vm_config.get('last_started', '从未启动')}\\n"
            
            QMessageBox.information(self, f"{vm_name} - 详情", details)
    
    def show_image_details(self, image_path):
        """显示镜像详情"""
        # TODO: 实现镜像详情显示
        QMessageBox.information(self, "镜像详情", f"镜像路径:\\n{image_path}")
    
    def show_storage_details(self, storage_path):
        """显示存储详情"""
        # TODO: 实现存储详情显示
        QMessageBox.information(self, "存储详情", f"存储路径:\\n{storage_path}")
    
    def new_vm(self):
        """新建虚拟机"""
        dialog = VMConfigDialog(None, self)
        if dialog.exec():
            self.load_data()  # 刷新数据
            QMessageBox.information(self, '成功', '虚拟机配置已创建')
    
    def edit_selected_vm(self):
        """编辑选中的虚拟机"""
        current_item = self.tree_widget.currentItem()
        if current_item:
            data = current_item.data(0, Qt.ItemDataRole.UserRole)
            if data and data[0] == 'vm':
                vm_name = data[1]
                dialog = VMConfigDialog(vm_name, self)
                if dialog.exec():
                    self.load_data()  # 刷新数据
                    QMessageBox.information(self, '成功', '虚拟机配置已更新')
    
    def open_snapshot_manager(self):
        """打开快照管理器"""
        current_item = self.tree_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择一个虚拟机")
            return
            
        data = current_item.data(0, Qt.ItemDataRole.UserRole)
        if data and data[0] == 'vm':
            vm_name = data[1]
            dialog = SnapshotDialog(vm_name, self.vm_controller, self)
            dialog.exec()
        else:
            QMessageBox.warning(self, "警告", "请选择一个虚拟机")
    
    def clone_selected_vm(self):
        """克隆选中的虚拟机"""
        current_item = self.tree_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择一个虚拟机")
            return
            
        data = current_item.data(0, Qt.ItemDataRole.UserRole)
        if data and data[0] == 'vm':
            source_vm_name = data[1]
            
            # 获取目标虚拟机名称
            target_vm_name, ok = QInputDialog.getText(
                self,
                "克隆虚拟机",
                f"请输入新虚拟机的名称 (基于 {source_vm_name}):",
                QLineEdit.EchoMode.Normal,
                f"{source_vm_name}_clone"
            )
            
            if ok and target_vm_name:
                if self.config_manager.vm_exists(target_vm_name):
                    QMessageBox.critical(self, "错误", f"虚拟机 '{target_vm_name}' 已存在")
                    return
                
                # 询问克隆类型
                clone_types = ["完全克隆", "链接克隆"]
                clone_type, ok = QInputDialog.getItem(
                    self,
                    "选择克隆类型",
                    "请选择克隆类型:",
                    clone_types,
                    0,
                    False
                )
                
                if ok:
                    actual_clone_type = "full" if clone_type == "完全克隆" else "linked"
                    
                    try:
                        success = self.clone_manager.clone_vm(
                            source_vm_name, target_vm_name, actual_clone_type
                        )
                        
                        if success:
                            QMessageBox.information(
                                self, "成功", 
                                f"虚拟机 '{source_vm_name}' 已成功克隆为 '{target_vm_name}'"
                            )
                            self.load_data()  # 刷新数据
                        else:
                            QMessageBox.critical(
                                self, "错误", 
                                f"克隆虚拟机失败"
                            )
                    except Exception as e:
                        QMessageBox.critical(
                            self, "错误", 
                            f"克隆虚拟机时发生错误:\n{str(e)}"
                        )
        else:
            QMessageBox.warning(self, "警告", "请选择一个虚拟机")
    
    def download_images(self):
        """下载镜像"""
        # 创建下载对话框
        dialog = DownloadImagesDialog(self.config_manager, self)
        dialog.exec()
        
        # 刷新数据
        self.load_data()
    
    def start_vm_with_options(self):
        """打开虚拟机启动选项对话框"""
        dialog = VMStartOptionsDialog(self)
        if dialog.exec():
            # TODO: 实现虚拟机启动逻辑
            cpu_count = dialog.cpu_count.value()
            memory_size = dialog.memory_size.value()
            system_disk = dialog.system_disk_path.text()
            network_mode = dialog.network_mode.text()
            vnc_port = dialog.vnc_port.value()
            boot_iso = dialog.boot_iso_path.text()
            
            # 导入启动线程
            from ..utils.vm_start_thread import VMStartThread
            
            # 创建并启动虚拟机
            self.vm_start_thread = VMStartThread(
                cpu_count=cpu_count,
                memory_size=memory_size,
                system_disk=system_disk,
                network_mode=network_mode,
                vnc_port=vnc_port,
                iso_path=boot_iso if boot_iso.strip() else None
            )
            
            # 连接信号
            self.vm_start_thread.started.connect(
                lambda msg: self.statusBar().showMessage(msg, 2000)
            )
            self.vm_start_thread.finished.connect(
                lambda msg, success: self.handle_vm_start_result(msg, success)
            )
            self.vm_start_thread.progress.connect(
                lambda msg: self.statusBar().showMessage(msg, 5000)
            )
            
            # 开始启动虚拟机
            self.vm_start_thread.start()
    
    def handle_vm_start_result(self, message, success):
        """处理虚拟机启动结果"""
        if success:
            QMessageBox.information(self, "虚拟机启动", message)
        else:
            QMessageBox.critical(self, "虚拟机启动失败", message)
    
    def manage_chrome_installation(self):
        """管理Chrome安装"""
        dialog = ChromeManagerDialog(self)
        dialog.exec()
    
    def cleanup_environment(self):
        """清理环境"""
        dialog = CleanupDialog(self)
        if dialog.exec():
            # TODO: 实现环境清理逻辑
            self.statusBar().showMessage('环境清理操作已记录，将在后台执行', 3000)
    
    def start_selected_vm(self):
        """启动选中的虚拟机"""
        current_item = self.tree_widget.currentItem()
        if current_item:
            data = current_item.data(0, Qt.ItemDataRole.UserRole)
            if data and data[0] == 'vm':
                vm_name = data[1]
                try:
                    # 从配置管理器获取配置
                    vm_config = self.config_manager.get_vm_config(vm_name)
                    if not vm_config:
                        QMessageBox.critical(self, '错误', f'未找到虚拟机配置: {vm_name}')
                        return
                    
                    from datetime import datetime
                    # 使用VM控制器启动
                    success = self.vm_controller.start_vm_with_config(vm_config)
                    if success:
                        # 更新配置中的状态
                        vm_config['status'] = 'running'
                        vm_config['last_started'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        self.config_manager.set_vm_config(vm_name, vm_config)
                        
                        self.load_vms()  # 只刷新虚拟机列表
                        QMessageBox.information(self, '成功', f'虚拟机 {vm_name} 已启动')
                    else:
                        QMessageBox.critical(self, '错误', f'启动虚拟机失败: {vm_name}')
                except Exception as e:
                    QMessageBox.critical(self, '错误', f'启动虚拟机失败:\\n{str(e)}')
    
    def stop_selected_vm(self):
        """停止选中的虚拟机"""
        current_item = self.tree_widget.currentItem()
        if current_item:
            data = current_item.data(0, Qt.ItemDataRole.UserRole)
            if data and data[0] == 'vm':
                vm_name = data[1]
                try:
                    # 使用VM控制器停止
                    success = self.vm_controller.stop_vm(vm_name)
                    if success:
                        # 更新配置中的状态
                        vm_config = self.config_manager.get_vm_config(vm_name)
                        if vm_config:
                            vm_config['status'] = 'stopped'
                            self.config_manager.set_vm_config(vm_name, vm_config)
                        
                        self.load_vms()  # 只刷新虚拟机列表
                        QMessageBox.information(self, '成功', f'虚拟机 {vm_name} 已停止')
                    else:
                        QMessageBox.critical(self, '错误', f'停止虚拟机失败: {vm_name}')
                except Exception as e:
                    QMessageBox.critical(self, '错误', f'停止虚拟机失败:\\n{str(e)}')
    
    def pause_selected_vm(self):
        """暂停选中的虚拟机"""
        # TODO: 实现虚拟机暂停功能
        QMessageBox.information(self, "暂停虚拟机", "暂停功能将在后续版本中实现")
    
    def refresh_data(self):
        """刷新数据"""
        self.load_data()
        self.statusBar().showMessage('数据已刷新', 2000)
    
    def backup_vm(self):
        """备份虚拟机"""
        # TODO: 实现虚拟机备份功能
        QMessageBox.information(self, "备份虚拟机", "备份功能将在后续版本中实现")
    
    def manage_vm_configs(self):
        """管理虚拟机配置"""
        vms = self.config_manager.list_vms()
        if not vms:
            QMessageBox.information(self, "虚拟机配置", "没有配置任何虚拟机")
            return
        
        vm_list = "\\n".join(vms)
        reply = QMessageBox.question(
            self, 
            "管理虚拟机配置", 
            f"已配置的虚拟机:\\n{vm_list}\\n\\n是否要编辑某个虚拟机的配置？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            vm_name, ok = QInputDialog.getItem(
                self,
                "选择虚拟机",
                "请选择要编辑的虚拟机:",
                vms,
                0,
                False
            )
            if ok and vm_name:
                self.edit_selected_vm()
    
    def manage_image_configs(self):
        """管理镜像文件配置"""
        images = self.config_manager.list_images()
        if not images:
            QMessageBox.information(self, "镜像文件配置", "没有配置任何镜像文件")
            return
        
        image_list = "\\n".join(images)
        QMessageBox.information(self, "镜像文件配置", f"已配置的镜像文件:\\n{image_list}")
    
    def open_system_check(self):
        """打开系统检测和修复工具"""
        dialog = SystemCheckDialog(self)
        dialog.exec()
    
    def open_storage_management(self):
        """打开存储管理"""
        dialog = StorageManagementDialog(self.storage_manager, self.config_manager, self)
        dialog.exec()
    
    def open_security_config(self):
        """打开安全配置"""
        dialog = SecurityConfigDialog(self.config_manager, self)
        dialog.exec()
    
    def open_security_audit(self):
        """打开安全审计"""
        dialog = SecurityAuditDialog(self.permission_manager, self)
        dialog.exec()
    
    def open_performance_report(self):
        """打开性能报告"""
        dialog = PerformanceReportDialog(self)
        dialog.exec()
    
    def open_settings(self):
        """打开设置"""
        dialog = SettingsDialog(self.config_manager, self)
        dialog.exec()
    
    def on_settings_changed(self):
        """设置更改后的回调"""
        # 重新应用主题
        current_theme = self.config_manager.get_global_config("theme") or "dark"
        self.theme_manager.set_theme(current_theme)
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            self.theme_manager.apply_theme(app)
    
    def change_theme(self, theme_name):
        """更改主题"""
        success = self.theme_manager.set_theme(theme_name)
        if success:
            # 重新应用主题到整个应用程序
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance()
            if app:
                self.theme_manager.apply_theme(app)
            
            theme_names = {"dark": "暗色", "light": "亮色", "blue": "蓝色"}
            theme_display_name = theme_names.get(theme_name, theme_name)
            QMessageBox.information(self, "主题更改", f"主题已更改为{theme_display_name}")
        else:
            QMessageBox.warning(self, "主题更改", "无效的主题名称")
    
    def about_dialog(self):
        """关于对话框"""
        QMessageBox.about(self, "关于 LTWin Manager", 
                         "LTWin Manager - 虚拟机管理软件\\n\\n版本: 1.0.0\\n\\n"
                         "一款基于PyQt6的虚拟机管理工具，用于管理QEMU/KVM虚拟机。")
    
    def update_resource_labels(self, system_info):
        """更新资源标签"""
        if isinstance(system_info, dict):
            cpu_percent = system_info.get('cpu_percent', 0)
            mem_info = system_info.get('memory', {})
            disk_info = system_info.get('disk', {})
            
            mem_used = mem_info.get('used_gb', 0)
            mem_total = mem_info.get('total_gb', 0)
            disk_used = disk_info.get('used_gb', 0)
            disk_total = disk_info.get('total_gb', 0)
            
            self.cpu_label.setText(f'CPU: {cpu_percent:.1f}%')
            self.mem_label.setText(f'内存: {mem_used:.1f}GB/{mem_total:.1f}GB')
            self.disk_label.setText(f'磁盘: {disk_used:.1f}GB/{disk_total:.1f}GB')
    
    def tray_icon_activated(self, reason):
        """处理托盘图标激活事件"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.showNormal()
            self.raise_()
            self.activateWindow()
    
    def closeEvent(self, event):
        """关闭事件处理"""
        # 最小化到系统托盘而不是直接退出
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            # 停止监控
            self.system_monitor.stop_monitoring()
            event.accept()