# -*- coding: utf-8 -*-
"""
系统监控工具
用于监控CPU、内存、磁盘等系统资源使用情况
"""

import psutil
import threading
import time
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from datetime import datetime


class SystemMonitor(QObject):
    # 自定义信号，用于更新UI
    resource_updated = pyqtSignal(dict)  # 传递包含所有系统信息的字典
    system_check_failed = pyqtSignal(str)  # 错误信息
    
    def __init__(self):
        super().__init__()
        self.monitoring = False
        self.monitor_thread = None
        self.check_interval = 2  # 监控间隔（秒）
        self.last_cpu_times = None
        self.last_cpu_timestamp = None
    
    def start_monitoring(self):
        """开始系统资源监控"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("系统监控已启动")
    
    def stop_monitoring(self):
        """停止系统资源监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        print("系统监控已停止")
    
    def _monitor_loop(self):
        """监控循环"""
        while self.monitoring:
            try:
                # 获取系统信息
                system_info = self._get_comprehensive_system_info()
                
                # 发送信号更新UI
                self.resource_updated.emit(system_info)
                
                # 等待指定时间后继续监控
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"监控出错: {e}")
                self.system_check_failed.emit(str(e))
                time.sleep(5)  # 出错后等待5秒再继续
    
    def _get_comprehensive_system_info(self):
        """获取综合系统信息"""
        # 获取CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # 获取CPU频率
        cpu_freq = psutil.cpu_freq()
        cpu_freq_current = cpu_freq.current if cpu_freq else 0
        cpu_freq_max = cpu_freq.max if cpu_freq else 0
        
        # 获取内存信息
        memory = psutil.virtual_memory()
        mem_total_gb = memory.total / (1024**3)
        mem_used_gb = memory.used / (1024**3)
        mem_percent = memory.percent
        
        # 获取交换内存信息
        swap = psutil.swap_memory()
        swap_total_gb = swap.total / (1024**3)
        swap_used_gb = swap.used / (1024**3)
        swap_percent = swap.percent
        
        # 获取磁盘信息（使用C盘或主分区）
        disk_partitions = psutil.disk_partitions()
        main_disk = disk_partitions[0]  # 默认使用第一个分区
        for partition in disk_partitions:
            if 'C:' in partition.mountpoint.upper() or partition.mountpoint == '/' or '/home' in partition.mountpoint:
                main_disk = partition
                break
        
        disk_usage = psutil.disk_usage(main_disk.mountpoint)
        disk_total_gb = disk_usage.total / (1024**3)
        disk_used_gb = disk_usage.used / (1024**3)
        disk_percent = disk_usage.percent
        
        # 获取网络IO信息
        net_io = psutil.net_io_counters()
        net_sent = net_io.bytes_sent / (1024**2)  # MB
        net_recv = net_io.bytes_recv / (1024**2)  # MB
        
        # 获取磁盘IO信息
        disk_io = psutil.disk_io_counters()
        disk_read = disk_io.read_bytes / (1024**2) if disk_io else 0  # MB
        disk_write = disk_io.write_bytes / (1024**2) if disk_io else 0  # MB
        
        # 获取进程数量
        process_count = len(psutil.pids())
        
        # 获取系统启动时间
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        
        # 构建系统信息字典
        system_info = {
            'cpu_percent': round(cpu_percent, 2),
            'cpu_freq_current': round(cpu_freq_current, 0),
            'cpu_freq_max': round(cpu_freq_max, 0),
            'memory': {
                'total_gb': round(mem_total_gb, 2),
                'used_gb': round(mem_used_gb, 2),
                'percent': mem_percent
            },
            'swap': {
                'total_gb': round(swap_total_gb, 2),
                'used_gb': round(swap_used_gb, 2),
                'percent': swap_percent
            },
            'disk': {
                'total_gb': round(disk_total_gb, 2),
                'used_gb': round(disk_used_gb, 2),
                'percent': disk_percent
            },
            'network': {
                'sent_mb': round(net_sent, 2),
                'recv_mb': round(net_recv, 2)
            },
            'disk_io': {
                'read_mb': round(disk_read, 2),
                'write_mb': round(disk_write, 2)
            },
            'process_count': process_count,
            'boot_time': boot_time,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        
        return system_info
    
    def get_system_info(self):
        """获取系统信息"""
        try:
            info = {
                'cpu_count': psutil.cpu_count(logical=False),
                'cpu_logical_count': psutil.cpu_count(logical=True),
                'cpu_freq': psutil.cpu_freq(),
                'memory_total': psutil.virtual_memory().total,
                'disk_partitions': [p.mountpoint for p in psutil.disk_partitions()],
                'platform': platform.platform(),
                'processor': platform.processor()
            }
            return info
        except Exception as e:
            print(f"获取系统信息失败: {e}")
            return {}
    
    def get_detailed_system_info(self):
        """获取详细的系统信息"""
        import platform
        try:
            boot_time = psutil.boot_time()
            uptime = time.time() - boot_time
            
            info = {
                'boot_time': time.ctime(boot_time),
                'uptime_seconds': int(uptime),
                'uptime_formatted': self.format_uptime(uptime),
                'cpu_times': psutil.cpu_times()._asdict(),
                'memory_info': psutil.virtual_memory()._asdict(),
                'swap_info': psutil.swap_memory()._asdict(),
                'disk_io': psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else {},
                'net_io': psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {},
                'system_platform': platform.platform(),
                'system_machine': platform.machine(),
                'system_processor': platform.processor(),
                'system_node': platform.node(),
                'process_count': len(psutil.pids()),
                'users': [user.name for user in psutil.users()]
            }
            return info
        except Exception as e:
            print(f"获取详细系统信息失败: {e}")
            return {}
    
    def format_uptime(self, seconds):
        """格式化运行时间"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{days}天 {hours}小时 {minutes}分钟"
