"""
虚拟机启动线程
"""

import subprocess
import threading
from PyQt6.QtCore import QThread, pyqtSignal


class VMStartThread(QThread):
    """
    用于启动虚拟机的后台线程
    """
    # 信号定义
    started = pyqtSignal(str)          # 启动通知
    finished = pyqtSignal(str, bool)   # 完成通知 (message, success)
    progress = pyqtSignal(str)         # 进度更新
    
    def __init__(self, cpu_count=6, memory_size=12, system_disk='win10.vmdk', 
                 network_mode='user', vnc_port=2, iso_path=None):
        super().__init__()
        self.cpu_count = cpu_count
        self.memory_size = memory_size
        self.system_disk = system_disk
        self.network_mode = network_mode
        self.vnc_port = vnc_port
        self.iso_path = iso_path
        
        # 线程控制
        self._stop_event = threading.Event()
    
    def run(self):
        """执行虚拟机启动命令"""
        try:
            self.started.emit('正在准备启动虚拟机...')
            
            # 构建QEMU命令
            cmd = [
                'qemu-system-x86_64',
                '-enable-kvm',
                f'-cpu', 'host',
                f'-smp', str(self.cpu_count),
                f'-m', f'{self.memory_size}G',
                '-M', 'q35',
                f'-drive', f'file={self.system_disk},if=virtio,cache=none,aio=io_uring,format=vmdk'
            ]
            
            # 添加ISO镜像（如果有）
            if self.iso_path and self.iso_path.strip():
                cmd.extend([
                    '-cdrom', self.iso_path
                ])
            
            # 添加网络配置
            cmd.extend([
                '-device', 'virtio-net-pci,netdev=net0',
                f'-netdev', f'{self.network_mode},id=net0'
            ])
            
            # 添加显卡和输入设备
            cmd.extend([
                '-vga', 'virtio',
                '-usb', '-device', 'usb-tablet'
            ])
            
            # 添加VNC
            cmd.append(f'-vnc :{self.vnc_port}')
            
            self.progress.emit(f'执行命令: {" ".join(cmd[:5])}...')  # 只显示部分命令避免过长
            
            # 执行命令
            self.progress.emit('正在启动虚拟机...')
            
            # 在Windows上可能需要使用subprocess.Popen
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30  # 30秒超时
            )
            
            if result.returncode == 0:
                self.finished.emit('虚拟机启动成功', True)
            else:
                self.finished.emit(f'虚拟机启动失败: {result.stderr}', False)
                
        except subprocess.TimeoutExpired:
            self.finished.emit('虚拟机启动超时', False)
        except FileNotFoundError:
            self.finished.emit('未找到QEMU命令，请确保已正确安装QEMU', False)
        except Exception as e:
            self.finished.emit(f'启动虚拟机时发生错误: {str(e)}', False)
    
    def stop(self):
        """停止线程"""
        self._stop_event.set()