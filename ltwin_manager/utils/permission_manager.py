# -*- coding: utf-8 -*-
"""
权限管理器
用于管理用户权限和操作控制
"""

import json
import hashlib
import secrets
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class User:
    """用户数据类"""
    username: str
    password_hash: str
    salt: str
    role: str = "user"  # admin, user, viewer
    created_at: str = ""
    last_login: str = ""
    is_active: bool = True


@dataclass
class Permission:
    """权限数据类"""
    name: str
    description: str
    allowed_actions: List[str]


class PermissionManager:
    """权限管理器"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.users_file = Path.home() / '.ltwin' / 'users.json'
        self.audit_log_file = Path.home() / '.ltwin' / 'audit.log'
        
        # 默认权限设置
        self.permissions = {
            'admin': Permission('Administrator', '管理员权限', [
                'vm_create', 'vm_edit', 'vm_delete', 'vm_start', 'vm_stop', 
                'vm_pause', 'vm_snapshot', 'vm_clone', 'system_config',
                'user_manage', 'audit_view'
            ]),
            'user': Permission('User', '普通用户权限', [
                'vm_create', 'vm_edit', 'vm_start', 'vm_stop', 'vm_snapshot'
            ]),
            'viewer': Permission('Viewer', '只读用户权限', [
                'vm_view', 'system_view'
            ])
        }
        
        self.users = self._load_users()
        self.current_user = None
    
    def _hash_password(self, password: str, salt: str) -> str:
        """哈希密码"""
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    
    def _generate_salt(self) -> str:
        """生成盐值"""
        return secrets.token_hex(32)
    
    def _load_users(self) -> Dict[str, User]:
        """加载用户信息"""
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    users = {}
                    for username, user_data in data.items():
                        users[username] = User(
                            username=user_data['username'],
                            password_hash=user_data['password_hash'],
                            salt=user_data['salt'],
                            role=user_data.get('role', 'user'),
                            created_at=user_data.get('created_at', ''),
                            last_login=user_data.get('last_login', ''),
                            is_active=user_data.get('is_active', True)
                        )
                    return users
            except Exception as e:
                print(f"加载用户信息失败: {e}")
        
        # 创建默认管理员账户
        default_admin = self._create_default_admin()
        return {default_admin.username: default_admin}
    
    def _create_default_admin(self) -> User:
        """创建默认管理员账户"""
        salt = self._generate_salt()
        password_hash = self._hash_password('admin123', salt)  # 默认密码
        
        admin_user = User(
            username='admin',
            password_hash=password_hash,
            salt=salt,
            role='admin',
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            is_active=True
        )
        
        # 保存用户信息
        temp_users = {admin_user.username: admin_user}
        self._save_users_to_dict(temp_users)
        
        return admin_user
    
    def _save_users(self):
        """保存用户信息"""
        data = {}
        for username, user in self.users.items():
            data[username] = {
                'username': user.username,
                'password_hash': user.password_hash,
                'salt': user.salt,
                'role': user.role,
                'created_at': user.created_at,
                'last_login': user.last_login,
                'is_active': user.is_active
            }
        
        self.users_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _save_users_to_dict(self, users_dict: Dict[str, User]):
        """将用户字典保存到文件"""
        data = {}
        for username, user in users_dict.items():
            data[username] = {
                'username': user.username,
                'password_hash': user.password_hash,
                'salt': user.salt,
                'role': user.role,
                'created_at': user.created_at,
                'last_login': user.last_login,
                'is_active': user.is_active
            }
        
        self.users_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """验证用户"""
        if username in self.users:
            user = self.users[username]
            if user.is_active:
                hashed_input = self._hash_password(password, user.salt)
                if hashed_input == user.password_hash:
                    user.last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.current_user = user
                    self._save_users()
                    self._log_audit(username, 'login_success', f'User {username} logged in')
                    return True
        
        self._log_audit(username, 'login_failure', f'Failed login attempt for user {username}')
        return False
    
    def register_user(self, username: str, password: str, role: str = 'user') -> bool:
        """注册新用户"""
        if username in self.users:
            return False  # 用户已存在
        
        if role not in self.permissions:
            return False  # 无效角色
        
        salt = self._generate_salt()
        password_hash = self._hash_password(password, salt)
        
        new_user = User(
            username=username,
            password_hash=password_hash,
            salt=salt,
            role=role,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            is_active=True
        )
        
        self.users[username] = new_user
        self._save_users()
        
        self._log_audit(self.current_user.username if self.current_user else 'system', 
                       'user_created', f'User {username} created with role {role}')
        return True
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """更改密码"""
        if username not in self.users:
            return False
        
        user = self.users[username]
        if not user.is_active:
            return False
        
        # 验证旧密码
        old_hashed = self._hash_password(old_password, user.salt)
        if old_hashed != user.password_hash:
            return False
        
        # 设置新密码
        new_salt = self._generate_salt()
        new_hashed = self._hash_password(new_password, new_salt)
        
        user.password_hash = new_hashed
        user.salt = new_salt
        
        self._save_users()
        self._log_audit(username, 'password_changed', f'Password changed for user {username}')
        return True
    
    def has_permission(self, action: str) -> bool:
        """检查当前用户是否有权限执行某操作"""
        if not self.current_user:
            return False  # 未登录用户没有权限
        
        if self.current_user.role not in self.permissions:
            return False
        
        perm = self.permissions[self.current_user.role]
        return action in perm.allowed_actions
    
    def get_user_role(self, username: str) -> Optional[str]:
        """获取用户角色"""
        if username in self.users:
            return self.users[username].role
        return None
    
    def update_user_role(self, target_username: str, new_role: str) -> bool:
        """更新用户角色（仅管理员可操作）"""
        if not self.current_user or self.current_user.role != 'admin':
            return False
        
        if target_username not in self.users or new_role not in self.permissions:
            return False
        
        old_role = self.users[target_username].role
        self.users[target_username].role = new_role
        self._save_users()
        
        self._log_audit(self.current_user.username, 'role_updated', 
                       f'Role for {target_username} changed from {old_role} to {new_role}')
        return True
    
    def deactivate_user(self, target_username: str) -> bool:
        """停用用户（仅管理员可操作）"""
        if not self.current_user or self.current_user.role != 'admin':
            return False
        
        if target_username not in self.users:
            return False
        
        self.users[target_username].is_active = False
        self._save_users()
        
        self._log_audit(self.current_user.username, 'user_deactivated', 
                       f'User {target_username} deactivated')
        return True
    
    def activate_user(self, target_username: str) -> bool:
        """激活用户（仅管理员可操作）"""
        if not self.current_user or self.current_user.role != 'admin':
            return False
        
        if target_username not in self.users:
            return False
        
        self.users[target_username].is_active = True
        self._save_users()
        
        self._log_audit(self.current_user.username, 'user_activated', 
                       f'User {target_username} activated')
        return True
    
    def _log_audit(self, username: str, action: str, details: str):
        """记录审计日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] USER: {username} | ACTION: {action} | DETAILS: {details}\n"
        
        try:
            with open(self.audit_log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"写入审计日志失败: {e}")
    
    def get_audit_logs(self, limit: int = 100) -> List[str]:
        """获取审计日志"""
        if not self.audit_log_file.exists():
            return []
        
        try:
            with open(self.audit_log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return lines[-limit:]  # 返回最后N条记录
        except Exception as e:
            print(f"读取审计日志失败: {e}")
            return []


# 全局权限管理器实例
permission_manager = None


def get_permission_manager(config_manager) -> PermissionManager:
    """获取权限管理器实例"""
    global permission_manager
    if permission_manager is None:
        permission_manager = PermissionManager(config_manager)
    return permission_manager