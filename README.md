# LTWin Manager - 企业级虚拟机管理平台 🚀

<div align="center">

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-3776ab.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-512bd4.svg?style=for-the-badge&logo=qt)](https://pypi.org/project/PyQt6/)
[![QEMU](https://img.shields.io/badge/QEMU-virtualization-4883b3.svg?style=for-the-badge&logo=qemu)](https://www.qemu.org/)
[![Platform](https://img.shields.io/badge/platform-Win%20|%20Linux%20|%20macOS-373a40.svg?style=for-the-badge)](https://github.com/lza6/LTWin-Manager)

✨ 一款现代化的虚拟机管理工具，让你的虚拟化世界触手可及 ✨  
🎯 轻松管理QEMU/KVM虚拟机，提升开发运维效率 🎯

[**⭐ GitHub 仓库**](https://github.com/lza6/LTWin-Manager) | [**📖 使用文档**](#使用教程) | [**🐛 问题反馈**](https://github.com/lza6/LTWin-Manager/issues) | [**🤝 贡献指南**](#贡献指南)

</div>

---

## 🌟 项目简介

LTWin Manager 是一款基于 **PyQt6** 的企业级虚拟机管理工具，专为简化 **QEMU/KVM** 虚拟机操作而设计。它提供了一个直观的图形界面，让用户能够轻松地创建、配置和管理虚拟机实例，无需复杂的命令行操作。

### 💡 为什么选择 LTWin Manager？

- 🎨 **现代化UI** - 直观美观的图形界面，支持多种主题
- 🔧 **功能丰富** - 虚拟机生命周期管理、快照、克隆、存储管理等
- ⚡ **性能卓越** - 高效的资源调度和性能监控
- 🔐 **安全可靠** - 基于角色的访问控制和安全审计
- 🌍 **跨平台支持** - Windows、Linux、macOS 通用

---

## 📚 目录结构

```
LTWin-Manager/
├── ltwin_manager/                 # 主程序目录
│   ├── __init__.py               # 包初始化
│   ├── main.py                   # 程序入口
│   ├── app_window.py             # 主窗口类
│   ├── controllers/              # 控制器层
│   │   └── vm_controller.py      # 虚拟机控制器
│   ├── ui/                       # UI界面组件
│   │   ├── dialogs/              # 对话框组件
│   │   │   ├── chrome_manager_dialog.py
│   │   │   ├── cleanup_dialog.py
│   │   │   ├── download_images_dialog.py
│   │   │   └── vm_start_options_dialog.py
│   │   ├── performance_report_dialog.py
│   │   ├── security_audit_dialog.py
│   │   ├── security_config_dialog.py
│   │   ├── settings_dialog.py
│   │   ├── snapshot_dialog.py
│   │   ├── storage_management_dialog.py
│   │   ├── system_check_dialog.py
│   │   ├── vm_config_dialog.py
│   │   ├── vm_details_panel.py
│   │   └── styles.qss           # 样式表
│   └── utils/                    # 工具类
│       ├── cleanup_tool.py       # 清理工具
│       ├── clone_manager.py      # 克隆管理
│       ├── config_manager.py     # 配置管理
│       ├── image_download_thread.py
│       ├── network_manager.py    # 网络管理
│       ├── performance_optimizer.py
│       ├── permission_manager.py # 权限管理
│       ├── snapshot_manager.py   # 快照管理
│       ├── storage_manager.py    # 存储管理
│       ├── system_checker.py     # 系统检测
│       ├── system_monitor.py     # 系统监控
│       ├── theme_manager.py      # 主题管理
│       └── vm_start_thread.py    # 虚拟机启动线程
├── README.md                     # 项目说明
├── SOFTWARE_PLAN.md              # 软件设计文档
├── requirements.txt              # 依赖包列表
├── run_ltwin.py                  # 启动脚本
├── quick_start.bat               # Windows快速启动脚本
├── setup_project.py              # 项目初始化脚本
├── launch.py                     # 启动器
├── final_test.py                 # 测试脚本
└── LICENSE                       # Apache 2.0许可证
```

---

## 🚀 快速开始

### 📦 安装要求

- **操作系统**: Windows 7+, Linux (Ubuntu 18.04+, CentOS 7+), macOS 10.14+
- **Python**: 3.8 或更高版本
- **内存**: 推荐 8GB RAM，最低 4GB
- **磁盘**: 至少 50GB 可用空间
- **虚拟化**: 支持 KVM (Linux) 或其他虚拟化技术

### 🛠️ 一键安装

#### 方法一：使用快速启动脚本（推荐）

```bash
# Windows用户
quick_start.bat
```

#### 方法二：手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/lza6/LTWin-Manager.git
cd LTWin-Manager

# 2. 创建虚拟环境（可选但推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动应用
python run_ltwin.py
```

### 🔧 安装QEMU（虚拟机功能必需）

#### Windows
从 [QEMU官网](https://www.qemu.org/download/#windows) 下载并安装

#### Linux
```bash
# Ubuntu/Debian
sudo apt install qemu-kvm

# CentOS/RHEL
sudo yum install qemu-kvm

# Arch Linux
sudo pacman -S qemu
```

#### macOS
```bash
# 使用Homebrew
brew install qemu
```

---

## 📖 使用教程

### 🎯 基础操作

#### 1. 创建虚拟机

1. **启动应用**：运行 `python run_ltwin.py`
2. **新建虚拟机**：
   - 点击菜单栏 `文件` → `新建虚拟机`
   - 或点击工具栏的 `新建虚拟机` 按钮
3. **配置虚拟机**：
   - **名称**：输入虚拟机名称
   - **CPU核心数**：建议 2-4 核
   - **内存**：建议 2048MB-4096MB
   - **磁盘路径**：选择虚拟磁盘保存位置
   - **ISO镜像**：选择系统安装镜像（可选）
4. **完成创建**：点击 `确定` 保存配置

#### 2. 启动虚拟机

1. **选择虚拟机**：在左侧资源管理器中选择要启动的虚拟机
2. **启动**：点击工具栏的 `启动` 按钮
3. **连接**：通过 VNC 客户端连接到指定端口

#### 3. 管理虚拟机

- **停止**：点击 `停止` 按钮
- **编辑配置**：右键虚拟机 → `编辑配置`
- **快照管理**：`管理` → `快照管理`
- **克隆虚拟机**：`管理` → `克隆虚拟机`

### 🎨 高级功能

#### 1. 快照管理

- **创建快照**：保存虚拟机当前状态
- **恢复快照**：回滚到之前的状态
- **删除快照**：清理不需要的快照

#### 2. 克隆功能

- **完全克隆**：创建完整的虚拟机副本
- **链接克隆**：节省磁盘空间的增量克隆

#### 3. 存储管理

- **虚拟磁盘管理**：创建、删除、扩容磁盘
- **ISO管理**：管理系统安装镜像
- **存储监控**：实时监控存储使用情况

#### 4. 网络配置

- **用户模式**：NAT网络，虚拟机可访问外网
- **桥接模式**：虚拟机获得独立IP
- **仅主机模式**：虚拟机与主机通信

### 🛡️ 安全特性

#### 1. 权限管理
- 基于角色的访问控制 (RBAC)
- 用户认证和授权
- 操作审计日志

#### 2. 安全配置
- 加密配置文件
- 安全的虚拟机隔离

---

## 🧠 技术架构详解

### 🏗️ 核心技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.8+ | 主编程语言 |
| **PyQt6** | 6.4+ | GUI框架 |
| **QEMU** | - | 虚拟化引擎 |
| **psutil** | 5.9+ | 系统监控 |
| **requests** | 2.28+ | HTTP请求 |
| **SQLAlchemy** | 2.0+ | ORM数据库 |
| **paramiko** | 3.0+ | SSH连接 |

### 🧩 架构模式

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   UI Layer      │    │  Business Logic │    │  Data Access    │
│                 │    │                 │    │                 │
│  - App Window   │◄──►│  - VM Controller│◄──►│  - Config Mgr   │
│  - Dialogs      │    │  - Network Mgr  │    │  - DB Models    │
│  - Panels       │    │  - Storage Mgr  │    │  - File I/O     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🎯 关键组件解析

#### 1. VMController (`ltwin_manager/controllers/vm_controller.py`)

这是虚拟机的核心控制器，负责虚拟机的生命周期管理：

```python
class VMController:
    def __init__(self, config_manager=None):
        self.vms = {}  # 虚拟机配置字典
        self.running_processes = {}  # 运行中的虚拟机进程
        self.config_manager = config_manager
```

**主要方法**：
- create_vm() - 创建虚拟机
- start_vm() - 启动虚拟机  
- stop_vm() - 停止虚拟机
- validate_config() - 验证配置

#### 2. ConfigManager (`ltwin_manager/utils/config_manager.py`)

配置管理器，负责持久化存储：

```python
class ConfigManager:
    def __init__(self):
        self.global_config_path = self.config_dir / 'config.json'
        self.vms_config_path = self.config_dir / 'vms.json'
        self.images_config_path = self.config_dir / 'images.json'
```

**功能**：
- 全局配置管理
- 虚拟机配置管理
- 镜像配置管理
- 自动备份/恢复

#### 3. SystemMonitor (`ltwin_manager/utils/system_monitor.py`)

系统监控组件，提供实时资源监控：

```python
class SystemMonitor(QObject):
    resource_updated = pyqtSignal(float, float, float, float, float)
```

**监控指标**：
- CPU使用率
- 内存使用情况
- 磁盘使用情况
- 网络流量

### 🔧 性能优化

#### 1. QEMU命令优化

```python
def optimize_qemu_command(self, base_cmd, vm_config):
    # 根据系统资源优化QEMU参数
    optimized_cmd = base_cmd + [
        '-enable-kvm',  # 启用硬件加速
        '-cpu', 'host', # 使用主机CPU特性
        '-smp', str(vm_config['cpu_cores']),
        '-m', str(vm_config['memory_mb']),
        '-M', 'q35',    # 使用现代芯片组
    ]
```

#### 2. 资源调度优化

- **内存管理**：智能分配虚拟机内存
- **CPU调度**：根据负载动态调整
- **磁盘I/O**：使用virtio驱动优化性能

---

## 📊 功能特性

### ✅ 已实现功能

| 功能 | 状态 | 描述 |
|------|------|------|
| **虚拟机管理** | ✅ 完成 | 创建、启动、停止、暂停、恢复 |
| **快照管理** | ✅ 完成 | 创建、恢复、删除快照 |
| **克隆功能** | ✅ 完成 | 完全克隆、链接克隆 |
| **存储管理** | ✅ 完成 | 虚拟磁盘管理、存储监控 |
| **网络配置** | ✅ 完成 | 多种网络模式支持 |
| **系统监控** | ✅ 完成 | CPU、内存、磁盘实时监控 |
| **主题管理** | ✅ 完成 | 多主题支持、个性化设置 |
| **权限管理** | ✅ 完成 | RBAC、安全审计 |
| **镜像下载** | ✅ 完成 | 集成常用镜像下载 |
| **性能优化** | ✅ 完成 | QEMU参数优化 |

### 🔄 开发中功能

| 功能 | 进度 | 计划 |
|------|------|------|
| **远程访问** | 70% | VNC、Web界面 |
| **集群管理** | 40% | 多节点管理 |
| **容器支持** | 30% | Docker容器集成 |
| **自动化部署** | 50% | 脚本化部署 |

### ❌ 待开发功能

| 功能 | 优先级 | 预期时间 |
|------|--------|----------|
| **云平台集成** | 高 | Q2 2024 |
| **机器学习优化** | 中 | Q3 2024 |
| **移动应用** | 低 | Q4 2024 |

---

## 🎯 使用场景

### 🏢 企业环境

- **开发测试**：快速搭建测试环境
- **持续集成**：CI/CD流水线虚拟机管理
- **培训演示**：标准化培训环境

### 👨‍💻 个人用户

- **学习实验**：安全的实验环境
- **软件兼容**：跨平台软件测试
- **游戏怀旧**：老游戏运行环境

### 🎓 教育机构

- **教学环境**：统一的教学平台
- **实验室**：批量虚拟机管理
- **考试系统**：隔离的考试环境

---

## ⚡ 性能基准

### 系统要求对比

| 配置 | 最低要求 | 推荐配置 | 最佳体验 |
|------|----------|----------|----------|
| **CPU** | 2核 | 4核 | 8核+ |
| **内存** | 4GB | 8GB | 16GB+ |
| **磁盘** | 20GB | 50GB | 100GB+ |
| **虚拟机数量** | 1-2台 | 3-5台 | 6台+ |

### 性能指标

- **启动时间**：平均 15-30 秒
- **响应延迟**：< 100ms
- **资源占用**：UI进程约 50-100MB 内存
- **并发支持**：最多 10 台虚拟机

---

## 🤝 贡献指南

### 🛠️ 开发环境设置

```bash
# 1. Fork 仓库
# 2. 克隆代码
git clone https://github.com/YOUR_USERNAME/LTWin-Manager.git
cd LTWin-Manager

# 3. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 4. 安装开发依赖
pip install -r requirements.txt

# 5. 运行测试
python -m pytest tests/
```

### 📝 代码规范

- **命名约定**：使用 snake_case
- **文档字符串**：遵循 Google 风格
- **类型注解**：函数参数和返回值
- **测试覆盖**：新增功能必须包含测试

### 🔄 Pull Request 流程

1. **Fork** 仓库
2. **创建分支**：`feature/your-feature-name`
3. **提交代码**：遵循提交信息规范
4. **发起PR**：详细描述变更内容
5. **代码审查**：等待维护者反馈

---

## 🔧 故障排除

### 🚨 常见问题

#### 1. 启动失败
```bash
# 检查Python版本
python --version

# 检查依赖
python setup_project.py

# 查看详细错误
python run_ltwin.py --verbose
```

#### 2. 虚拟机无法启动
- 检查QEMU是否安装
- 确认虚拟化技术已启用
- 检查配置文件路径

#### 3. 性能问题
- 关闭不必要的虚拟机
- 检查系统资源使用
- 调整QEMU参数

### 📞 技术支持

- **GitHub Issues**: [问题反馈](https://github.com/lza6/LTWin-Manager/issues)
- **邮件支持**: support@ltwin-manager.com
- **社区论坛**: 计划中...

---

## 🚀 未来发展

### 📈 短期规划 (6个月内)

- **容器集成**：Docker容器管理
- **云平台对接**：AWS、Azure、阿里云
- **移动端应用**：手机和平板支持

### 🌟 中长期愿景 (1-3年)

- **AI优化**：智能资源调度
- **边缘计算**：分布式虚拟机管理
- **区块链集成**：安全可信的虚拟机管理

### 🎯 技术路线图

```
2024 Q1: 容器集成 & 云平台对接
2024 Q2: AI性能优化
2024 Q3: 移动端应用
2024 Q4: 边缘计算支持
2025+: 区块链集成 & 更多创新
```

---

## 💡 设计哲学

### 🎨 用户体验优先

我们坚信，优秀的工具应该让复杂的事情变得简单。LTWin Manager 的设计理念是：

- **简洁直观**：减少学习成本
- **功能强大**：满足专业需求
- **稳定可靠**：保证生产环境安全

### 🔧 开发者友好

- **模块化设计**：易于扩展和维护
- **清晰文档**：详尽的API文档
- **活跃社区**：持续的技术支持

### 🌍 开源精神

- **透明开发**：公开开发过程
- **协作共建**：欢迎社区贡献
- **知识共享**：推广虚拟化技术

---

## 🎉 社区参与

### 📣 分享你的故事

使用 LTWin Manager 进行了有趣的项目？解决了复杂的问题？我们很乐意听到你的故事！

### 🌟 Star 和分享

如果你喜欢这个项目，请给我们一个 Star ⭐ 并分享给更多的人！

### 🤝 贡献代码

无论是一个小的 bug 修复还是一个大的功能增强，我们都欢迎你的贡献！

---

## 📜 许可证

```
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Copyright 2024 LTWin Manager Project

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

## 🙏 致谢

感谢所有为 LTWin Manager 项目做出贡献的开发者和用户！特别感谢：

- **QEMU/KVM** 团队 - 提供了强大的虚拟化技术
- **PyQt6** 开发者 - 优秀的GUI框架
- **Python社区** - 强大的生态系统
- **所有贡献者** - 让项目更加完善

---

<div align="center">

### 🌟 让我们一起构建更美好的虚拟化世界！🌟

[**⭐ 立即开始使用**](https://github.com/lza6/LTWin-Manager) | [**🤝 贡献代码**](CONTRIBUTING.md) | [**📜 查看许可证**](LICENSE)

_LTWin Manager - 让虚拟化管理变得简单而强大_

</div>