# -*- coding: utf-8 -*-
"""
安全配置对话框
用于配置系统安全设置
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QGroupBox, QPushButton, QLabel, QSpinBox,
    QCheckBox, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt


class SecurityConfigDialog(QDialog):
    """安全配置对话框"""
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        
        self.setWindowTitle("安全配置")
        self.resize(500, 400)
        
        self.init_ui()
        self.load_security_settings()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 登录安全设置
        login_security_group = QGroupBox("登录安全")
        login_security_layout = QFormLayout(login_security_group)
        
        self.max_login_attempts_spin = QSpinBox()
        self.max_login_attempts_spin.setRange(1, 10)
        self.max_login_attempts_spin.setValue(5)
        login_security_layout.addRow("最大登录尝试次数:", self.max_login_attempts_spin)
        
        self.login_lockout_duration_spin = QSpinBox()
        self.login_lockout_duration_spin.setRange(1, 60)
        self.login_lockout_duration_spin.setValue(15)
        self.login_lockout_duration_spin.setSuffix(" 分钟")
        login_security_layout.addRow("账户锁定时长:", self.login_lockout_duration_spin)
        
        self.enable_captcha_check = QCheckBox("启用验证码")
        login_security_layout.addRow("", self.enable_captcha_check)
        
        layout.addWidget(login_security_group)
        
        # 密码策略设置
        pwd_policy_group = QGroupBox("密码策略")
        pwd_policy_layout = QFormLayout(pwd_policy_group)
        
        self.min_pwd_length_spin = QSpinBox()
        self.min_pwd_length_spin.setRange(6, 20)
        self.min_pwd_length_spin.setValue(8)
        self.min_pwd_length_spin.setSuffix(" 位")
        pwd_policy_layout.addRow("最小密码长度:", self.min_pwd_length_spin)
        
        self.require_upper_check = QCheckBox("必须包含大写字母")
        pwd_policy_layout.addRow("", self.require_upper_check)
        
        self.require_lower_check = QCheckBox("必须包含小写字母")
        pwd_policy_layout.addRow("", self.require_lower_check)
        
        self.require_number_check = QCheckBox("必须包含数字")
        pwd_policy_layout.addRow("", self.require_number_check)
        
        self.require_special_check = QCheckBox("必须包含特殊字符")
        pwd_policy_layout.addRow("", self.require_special_check)
        
        self.pwd_expiry_days_spin = QSpinBox()
        self.pwd_expiry_days_spin.setRange(30, 365)
        self.pwd_expiry_days_spin.setValue(90)
        self.pwd_expiry_days_spin.setSuffix(" 天")
        pwd_policy_layout.addRow("密码过期天数:", self.pwd_expiry_days_spin)
        
        layout.addWidget(pwd_policy_group)
        
        # 审计日志设置
        audit_group = QGroupBox("审计日志")
        audit_layout = QFormLayout(audit_group)
        
        self.log_retention_days_spin = QSpinBox()
        self.log_retention_days_spin.setRange(7, 365)
        self.log_retention_days_spin.setValue(90)
        self.log_retention_days_spin.setSuffix(" 天")
        audit_layout.addRow("日志保留天数:", self.log_retention_days_spin)
        
        self.enable_detailed_logging_check = QCheckBox("启用详细操作日志")
        audit_layout.addRow("", self.enable_detailed_logging_check)
        
        layout.addWidget(audit_group)
        
        # 数据加密设置
        encryption_group = QGroupBox("数据加密")
        encryption_layout = QFormLayout(encryption_group)
        
        self.encrypt_config_check = QCheckBox("加密配置文件")
        encryption_layout.addRow("", self.encrypt_config_check)
        
        self.encryption_method_combo = QLineEdit()
        self.encryption_method_combo.setText("AES-256")
        self.encryption_method_combo.setReadOnly(True)
        encryption_layout.addRow("加密算法:", self.encryption_method_combo)
        
        layout.addWidget(encryption_group)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.reset_defaults_btn = QPushButton("恢复默认设置")
        self.reset_defaults_btn.clicked.connect(self.reset_to_defaults)
        
        self.apply_btn = QPushButton("应用")
        self.apply_btn.clicked.connect(self.apply_settings)
        
        self.ok_btn = QPushButton("确定")
        self.ok_btn.clicked.connect(self.accept)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.reset_defaults_btn)
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
    
    def load_security_settings(self):
        """加载安全设置"""
        # 加载登录安全设置
        max_attempts = self.config_manager.get_global_config("security_max_login_attempts")
        self.max_login_attempts_spin.setValue(max_attempts or 5)
        
        lockout_duration = self.config_manager.get_global_config("security_login_lockout_duration")
        self.login_lockout_duration_spin.setValue(lockout_duration or 15)
        
        enable_captcha = self.config_manager.get_global_config("security_enable_captcha")
        self.enable_captcha_check.setChecked(enable_captcha or False)
        
        # 加载密码策略设置
        min_pwd_length = self.config_manager.get_global_config("security_min_password_length")
        self.min_pwd_length_spin.setValue(min_pwd_length or 8)
        
        require_upper = self.config_manager.get_global_config("security_require_uppercase")
        self.require_upper_check.setChecked(require_upper or True)
        
        require_lower = self.config_manager.get_global_config("security_require_lowercase")
        self.require_lower_check.setChecked(require_lower or True)
        
        require_number = self.config_manager.get_global_config("security_require_number")
        self.require_number_check.setChecked(require_number or True)
        
        require_special = self.config_manager.get_global_config("security_require_special_char")
        self.require_special_check.setChecked(require_special or False)
        
        pwd_expiry = self.config_manager.get_global_config("security_password_expiry_days")
        self.pwd_expiry_days_spin.setValue(pwd_expiry or 90)
        
        # 加载审计日志设置
        log_retention = self.config_manager.get_global_config("security_log_retention_days")
        self.log_retention_days_spin.setValue(log_retention or 90)
        
        enable_detailed = self.config_manager.get_global_config("security_enable_detailed_logging")
        self.enable_detailed_logging_check.setChecked(enable_detailed or True)
        
        # 加载数据加密设置
        encrypt_config = self.config_manager.get_global_config("security_encrypt_config")
        self.encrypt_config_check.setChecked(encrypt_config or False)
    
    def apply_settings(self):
        """应用设置"""
        # 保存登录安全设置
        self.config_manager.set_global_config("security_max_login_attempts", self.max_login_attempts_spin.value())
        self.config_manager.set_global_config("security_login_lockout_duration", self.login_lockout_duration_spin.value())
        self.config_manager.set_global_config("security_enable_captcha", self.enable_captcha_check.isChecked())
        
        # 保存密码策略设置
        self.config_manager.set_global_config("security_min_password_length", self.min_pwd_length_spin.value())
        self.config_manager.set_global_config("security_require_uppercase", self.require_upper_check.isChecked())
        self.config_manager.set_global_config("security_require_lowercase", self.require_lower_check.isChecked())
        self.config_manager.set_global_config("security_require_number", self.require_number_check.isChecked())
        self.config_manager.set_global_config("security_require_special_char", self.require_special_check.isChecked())
        self.config_manager.set_global_config("security_password_expiry_days", self.pwd_expiry_days_spin.value())
        
        # 保存审计日志设置
        self.config_manager.set_global_config("security_log_retention_days", self.log_retention_days_spin.value())
        self.config_manager.set_global_config("security_enable_detailed_logging", self.enable_detailed_logging_check.isChecked())
        
        # 保存数据加密设置
        self.config_manager.set_global_config("security_encrypt_config", self.encrypt_config_check.isChecked())
        
        QMessageBox.information(self, "应用成功", "安全配置已应用")
    
    def reset_to_defaults(self):
        """恢复默认设置"""
        reply = QMessageBox.question(
            self,
            "确认操作",
            "确定要恢复默认安全设置吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 重置为默认值
            self.max_login_attempts_spin.setValue(5)
            self.login_lockout_duration_spin.setValue(15)
            self.enable_captcha_check.setChecked(False)
            
            self.min_pwd_length_spin.setValue(8)
            self.require_upper_check.setChecked(True)
            self.require_lower_check.setChecked(True)
            self.require_number_check.setChecked(True)
            self.require_special_check.setChecked(False)
            self.pwd_expiry_days_spin.setValue(90)
            
            self.log_retention_days_spin.setValue(90)
            self.enable_detailed_logging_check.setChecked(True)
            
            self.encrypt_config_check.setChecked(False)
    
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
    dialog = SecurityConfigDialog(config_manager)
    dialog.show()
    sys.exit(app.exec())