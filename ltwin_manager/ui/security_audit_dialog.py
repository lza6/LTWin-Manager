# -*- coding: utf-8 -*-
"""
安全审计对话框
用于显示系统安全审计信息
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QTabWidget, QWidget, QGroupBox, QPushButton,
    QLabel, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QHeaderView, QMessageBox, QSpinBox, QLineEdit,
    QComboBox
)
from PyQt6.QtCore import Qt


class SecurityAuditDialog(QDialog):
    """安全审计对话框"""
    
    def __init__(self, permission_manager, parent=None):
        super().__init__(parent)
        self.permission_manager = permission_manager
        
        self.setWindowTitle("安全审计")
        self.resize(900, 600)
        
        self.init_ui()
        self.load_security_info()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 用户管理标签页
        user_mgmt_tab = self.create_user_management_tab()
        tab_widget.addTab(user_mgmt_tab, "用户管理")
        
        # 权限管理标签页
        perm_mgmt_tab = self.create_permission_management_tab()
        tab_widget.addTab(perm_mgmt_tab, "权限管理")
        
        # 审计日志标签页
        audit_log_tab = self.create_audit_log_tab()
        tab_widget.addTab(audit_log_tab, "审计日志")
        
        # 安全设置标签页
        security_settings_tab = self.create_security_settings_tab()
        tab_widget.addTab(security_settings_tab, "安全设置")
        
        layout.addWidget(tab_widget)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self.load_security_info)
        
        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
    
    def create_user_management_tab(self):
        """创建用户管理标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 用户列表
        self.users_tree = QTreeWidget()
        self.users_tree.setHeaderLabels(["用户名", "角色", "状态", "创建时间", "最后登录"])
        header = self.users_tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(QLabel("用户列表:"))
        layout.addWidget(self.users_tree)
        
        # 用户操作组
        user_ops_group = QGroupBox("用户操作")
        user_ops_layout = QFormLayout(user_ops_group)
        
        # 添加用户
        add_user_layout = QHBoxLayout()
        self.new_username_edit = QLineEdit()
        self.new_username_edit.setPlaceholderText("新用户名")
        self.new_password_edit = QLineEdit()
        self.new_password_edit.setPlaceholderText("密码")
        self.new_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_role_combo = QComboBox()
        self.new_role_combo.addItems(["admin", "user", "viewer"])
        
        add_user_layout.addWidget(QLabel("用户名:"))
        add_user_layout.addWidget(self.new_username_edit)
        add_user_layout.addWidget(QLabel("密码:"))
        add_user_layout.addWidget(self.new_password_edit)
        add_user_layout.addWidget(QLabel("角色:"))
        add_user_layout.addWidget(self.new_role_combo)
        
        self.add_user_btn = QPushButton("添加用户")
        self.add_user_btn.clicked.connect(self.add_user)
        add_user_layout.addWidget(self.add_user_btn)
        
        user_ops_layout.addRow(add_user_layout)
        
        # 修改用户
        mod_user_layout = QHBoxLayout()
        self.mod_username_edit = QLineEdit()
        self.mod_username_edit.setPlaceholderText("用户名")
        self.mod_role_combo = QComboBox()
        self.mod_role_combo.addItems(["admin", "user", "viewer"])
        
        mod_user_layout.addWidget(QLabel("用户名:"))
        mod_user_layout.addWidget(self.mod_username_edit)
        mod_user_layout.addWidget(QLabel("新角色:"))
        mod_user_layout.addWidget(self.mod_role_combo)
        
        self.mod_user_btn = QPushButton("修改角色")
        self.mod_user_btn.clicked.connect(self.modify_user)
        mod_user_layout.addWidget(self.mod_user_btn)
        
        self.deactivate_user_btn = QPushButton("停用用户")
        self.deactivate_user_btn.clicked.connect(self.deactivate_user)
        mod_user_layout.addWidget(self.deactivate_user_btn)
        
        self.activate_user_btn = QPushButton("激活用户")
        self.activate_user_btn.clicked.connect(self.activate_user)
        mod_user_layout.addWidget(self.activate_user_btn)
        
        user_ops_layout.addRow(mod_user_layout)
        
        layout.addWidget(user_ops_group)
        
        return widget
    
    def create_permission_management_tab(self):
        """创建权限管理标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 权限列表
        self.perm_tree = QTreeWidget()
        self.perm_tree.setHeaderLabels(["角色", "权限", "描述"])
        header = self.perm_tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(QLabel("权限配置:"))
        layout.addWidget(self.perm_tree)
        
        # 权限说明
        perm_desc_group = QGroupBox("权限说明")
        perm_desc_layout = QVBoxLayout(perm_desc_group)
        
        perm_desc_text = QTextEdit()
        perm_desc_text.setReadOnly(True)
        perm_desc_text.setPlainText("""
        权限说明：
        
        admin: 管理员权限，拥有所有操作权限
        - 虚拟机创建、编辑、删除
        - 系统配置管理
        - 用户管理
        - 审计日志查看
        
        user: 普通用户权限
        - 虚拟机创建、编辑、启动、停止
        - 快照管理
        
        viewer: 只读用户权限
        - 虚拟机信息查看
        - 系统信息查看
        """)
        
        perm_desc_layout.addWidget(perm_desc_text)
        layout.addWidget(perm_desc_group)
        
        return widget
    
    def create_audit_log_tab(self):
        """创建审计日志标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 审计日志显示
        self.audit_log_text = QTextEdit()
        self.audit_log_text.setReadOnly(True)
        
        layout.addWidget(QLabel("审计日志:"))
        layout.addWidget(self.audit_log_text)
        
        # 日志操作
        log_ops_layout = QHBoxLayout()
        
        self.log_limit_spin = QSpinBox()
        self.log_limit_spin.setRange(10, 1000)
        self.log_limit_spin.setValue(100)
        log_ops_layout.addWidget(QLabel("显示条数:"))
        log_ops_layout.addWidget(self.log_limit_spin)
        
        self.refresh_log_btn = QPushButton("刷新日志")
        self.refresh_log_btn.clicked.connect(self.refresh_audit_log)
        log_ops_layout.addWidget(self.refresh_log_btn)
        
        self.clear_log_btn = QPushButton("清除日志")
        self.clear_log_btn.clicked.connect(self.clear_audit_log)
        log_ops_layout.addWidget(self.clear_log_btn)
        
        log_ops_layout.addStretch()
        
        layout.addLayout(log_ops_layout)
        
        return widget
    
    def create_security_settings_tab(self):
        """创建安全设置标签页"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # 密码策略设置
        pwd_policy_group = QGroupBox("密码策略")
        pwd_policy_layout = QFormLayout(pwd_policy_group)
        
        self.min_pwd_length_spin = QSpinBox()
        self.min_pwd_length_spin.setRange(6, 20)
        self.min_pwd_length_spin.setValue(8)
        pwd_policy_layout.addRow("最小密码长度:", self.min_pwd_length_spin)
        
        self.require_upper_check = QPushButton("需要大写字母")
        self.require_upper_check.setCheckable(True)
        self.require_upper_check.setChecked(True)
        pwd_policy_layout.addRow("", self.require_upper_check)
        
        self.require_lower_check = QPushButton("需要小写字母")
        self.require_lower_check.setCheckable(True)
        self.require_lower_check.setChecked(True)
        pwd_policy_layout.addRow("", self.require_lower_check)
        
        self.require_number_check = QPushButton("需要数字")
        self.require_number_check.setCheckable(True)
        self.require_number_check.setChecked(True)
        pwd_policy_layout.addRow("", self.require_number_check)
        
        layout.addWidget(pwd_policy_group)
        
        # 登录安全设置
        login_sec_group = QGroupBox("登录安全")
        login_sec_layout = QFormLayout(login_sec_group)
        
        self.max_attempts_spin = QSpinBox()
        self.max_attempts_spin.setRange(3, 10)
        self.max_attempts_spin.setValue(5)
        login_sec_layout.addRow("最大尝试次数:", self.max_attempts_spin)
        
        self.lockout_duration_spin = QSpinBox()
        self.lockout_duration_spin.setRange(1, 60)
        self.lockout_duration_spin.setValue(15)
        self.lockout_duration_spin.setSuffix(" 分钟")
        login_sec_layout.addRow("锁定时长:", self.lockout_duration_spin)
        
        layout.addWidget(login_sec_group)
        
        return widget
    
    def load_security_info(self):
        """加载安全信息"""
        self.load_users_list()
        self.load_permissions_list()
        self.refresh_audit_log()
    
    def load_users_list(self):
        """加载用户列表"""
        self.users_tree.clear()
        
        for username, user in self.permission_manager.users.items():
            item = QTreeWidgetItem([
                user.username,
                user.role,
                "活跃" if user.is_active else "已停用",
                user.created_at,
                user.last_login
            ])
            self.users_tree.addTopLevelItem(item)
    
    def load_permissions_list(self):
        """加载权限列表"""
        self.perm_tree.clear()
        
        for role_name, perm in self.permission_manager.permissions.items():
            for action in perm.allowed_actions:
                item = QTreeWidgetItem([role_name, action, perm.description])
                self.perm_tree.addTopLevelItem(item)
    
    def refresh_audit_log(self):
        """刷新审计日志"""
        limit = self.log_limit_spin.value()
        logs = self.permission_manager.get_audit_logs(limit)
        self.audit_log_text.setPlainText("".join(logs))
    
    def clear_audit_log(self):
        """清除审计日志"""
        reply = QMessageBox.question(
            self,
            "确认清除",
            "确定要清除所有审计日志吗？此操作不可撤销！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with open(self.permission_manager.audit_log_file, 'w') as f:
                    f.write("")
                self.audit_log_text.clear()
                QMessageBox.information(self, "清除完成", "审计日志已清除")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"清除日志失败: {str(e)}")
    
    def add_user(self):
        """添加用户"""
        username = self.new_username_edit.text().strip()
        password = self.new_password_edit.text()
        role = self.new_role_combo.currentText()
        
        if not username or not password:
            QMessageBox.warning(self, "输入错误", "用户名和密码不能为空")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "输入错误", "密码长度不能少于6位")
            return
        
        success = self.permission_manager.register_user(username, password, role)
        if success:
            QMessageBox.information(self, "成功", f"用户 {username} 创建成功")
            self.new_username_edit.clear()
            self.new_password_edit.clear()
            self.load_users_list()
        else:
            QMessageBox.critical(self, "错误", f"创建用户失败，用户可能已存在或角色无效")
    
    def modify_user(self):
        """修改用户角色"""
        username = self.mod_username_edit.text().strip()
        new_role = self.mod_role_combo.currentText()
        
        if not username:
            QMessageBox.warning(self, "输入错误", "请输入用户名")
            return
        
        success = self.permission_manager.update_user_role(username, new_role)
        if success:
            QMessageBox.information(self, "成功", f"用户 {username} 角色已更新为 {new_role}")
            self.mod_username_edit.clear()
            self.load_users_list()
        else:
            QMessageBox.critical(self, "错误", f"更新用户角色失败，请检查权限或用户名是否存在")
    
    def deactivate_user(self):
        """停用用户"""
        username = self.mod_username_edit.text().strip()
        
        if not username:
            QMessageBox.warning(self, "输入错误", "请输入用户名")
            return
        
        success = self.permission_manager.deactivate_user(username)
        if success:
            QMessageBox.information(self, "成功", f"用户 {username} 已停用")
            self.load_users_list()
        else:
            QMessageBox.critical(self, "错误", f"停用用户失败，请检查权限或用户名是否存在")
    
    def activate_user(self):
        """激活用户"""
        username = self.mod_username_edit.text().strip()
        
        if not username:
            QMessageBox.warning(self, "输入错误", "请输入用户名")
            return
        
        success = self.permission_manager.activate_user(username)
        if success:
            QMessageBox.information(self, "成功", f"用户 {username} 已激活")
            self.load_users_list()
        else:
            QMessageBox.critical(self, "错误", f"激活用户失败，请检查权限或用户名是否存在")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    from ltwin_manager.utils.permission_manager import get_permission_manager
    from ltwin_manager.utils.config_manager import get_config_manager
    
    app = QApplication(sys.argv)
    config_manager = get_config_manager()
    permission_manager = get_permission_manager(config_manager)
    dialog = SecurityAuditDialog(permission_manager)
    dialog.show()
    sys.exit(app.exec())