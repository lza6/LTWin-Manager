# -*- coding: utf-8 -*-
"""
性能优化器
用于优化虚拟机性能和系统资源分配
"""

import subprocess
import psutil
import platform
from typing import Dict, List, Optional
from pathlib import Path


class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.is_kvm_supported = self._check_kvm_support()
        self.recommended_settings = self._get_recommended_settings()
    
    def _check_kvm_support(self) -> bool:
        """检查KVM支持"""
        try:
            if self.system == "linux":
                # 检查KVM模块是否加载
                result = subprocess.run(['lsmod'], capture_output=True, text=True)
                return 'kvm' in result.stdout and 'kvm_intel' in result.stdout or 'kvm_amd' in result.stdout
            elif self.system == "windows":
                # Windows上检查Hyper-V或WSL2
                try:
                    result = subprocess.run(['systeminfo', '|', 'findstr', 'Hyper-V'], 
                                          shell=True, capture_output=True, text=True)
                    return len(result.stdout) > 0
                except:
                    return False
            else:
                return False
        except:
            return False
    
    def _get_recommended_settings(self) -> Dict:
        """获取推荐的虚拟机设置"""
        total_memory = psutil.virtual_memory().total
        total_memory_gb = total_memory / (1024**3)
        cpu_count = psutil.cpu_count(logical=False)
        
        # 根据系统资源推荐虚拟机配置
        recommended_cpu = max(1, min(cpu_count - 2, 8))  # 保留2个核心给宿主机，最多8个
        recommended_memory = min(int(total_memory_gb * 0.6), 8192)  # 使用60%的内存，最多8GB
        
        return {
            'recommended_cpu': recommended_cpu,
            'recommended_memory_mb': recommended_memory,
            'recommended_disk_size_gb': 40,  # 推荐40GB磁盘
            'is_kvm_supported': self.is_kvm_supported,
            'total_system_memory_gb': round(total_memory_gb, 2),
            'total_cpu_cores': cpu_count
        }
    
    def optimize_qemu_command(self, base_cmd: List[str], vm_config: Dict) -> List[str]:
        """
        优化QEMU命令参数
        
        Args:
            base_cmd: 基础QEMU命令
            vm_config: 虚拟机配置
        
        Returns:
            优化后的QEMU命令
        """
        optimized_cmd = base_cmd.copy()
        
        # 根据配置优化参数
        cpu_cores = vm_config.get('cpu_cores', 2)
        
        # 添加性能优化参数
        if self.system == "linux" and self.is_kvm_supported:
            # 使用KVM加速
            if '-enable-kvm' not in optimized_cmd:
                optimized_cmd.insert(1, '-enable-kvm')
        
        # 优化内存后端
        optimized_cmd.extend([
            '-mem-prealloc',  # 预分配内存
            '-m', str(vm_config.get('memory_mb', 2048)),
            '-smp', f'cpus={cpu_cores},cores={cpu_cores}',  # 优化SMP配置
        ])
        
        # 优化存储性能
        disk_path = vm_config.get('disk_path', '')
        if disk_path:
            # 使用优化的存储参数
            for i, arg in enumerate(optimized_cmd):
                if 'drive' in arg and disk_path in optimized_cmd[min(i+1, len(optimized_cmd)-1)]:
                    # 替换为性能更好的参数
                    optimized_cmd[i+1] = optimized_cmd[i+1].replace(
                        'cache=none,aio=io_uring', 
                        'cache=none,aio=native,cache.direct=on,cache.no-flush=on'
                    )
                    break
        
        # 优化网络性能
        optimized_cmd.extend([
            '-netdev', f'user,id=net0,hostfwd=tcp::{vm_config.get("vnc_port", 5900)}-:5900',
            '-device', 'virtio-net-pci,netdev=net0,romfile='  # 禁用ROM文件以提升性能
        ])
        
        # 优化显示性能
        optimized_cmd.extend([
            '-vga', 'virtio',  # 使用virtio显卡
            '-display', 'gtk,zoom-to-fit=off',  # 如果使用GTK显示
        ])
        
        # 添加性能优化标志
        optimized_cmd.extend([
            '-nodefaults',  # 禁用默认设备
            '-no-user-config',  # 不加载用户配置
        ])
        
        return optimized_cmd
    
    def get_system_performance_tips(self) -> List[str]:
        """获取系统性能优化建议"""
        tips = []
        
        # 内存使用建议
        memory = psutil.virtual_memory()
        if memory.percent > 80:
            tips.append("系统内存使用率较高，建议关闭不必要的应用程序")
        
        # CPU使用建议
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 80:
            tips.append("CPU使用率较高，考虑减少虚拟机CPU核心数")
        
        # 磁盘性能建议
        disk_usage = psutil.disk_usage('/')
        if disk_usage.percent > 80:
            tips.append("磁盘空间不足，建议清理磁盘空间以获得更好的虚拟机性能")
        
        # KVM支持建议
        if not self.is_kvm_supported:
            tips.append("系统不支持硬件虚拟化加速(KVM)，虚拟机性能可能较低")
        
        # 推荐配置
        tips.append(f"推荐虚拟机配置: {self.recommended_settings['recommended_cpu']} "
                   f"个CPU核心, {self.recommended_settings['recommended_memory_mb']} MB内存")
        
        return tips if tips else ["系统性能良好，无需特别优化"]
    
    def get_vm_performance_recommendations(self, vm_config: Dict) -> List[str]:
        """获取虚拟机性能优化建议"""
        recommendations = []
        
        # 检查CPU配置
        cpu_cores = vm_config.get('cpu_cores', 2)
        if cpu_cores > self.recommended_settings['recommended_cpu']:
            recommendations.append(f"虚拟机CPU核心数({cpu_cores})过高，"
                                 f"建议调整为{self.recommended_settings['recommended_cpu']}个")
        
        # 检查内存配置
        memory_mb = vm_config.get('memory_mb', 2048)
        if memory_mb > self.recommended_settings['recommended_memory_mb']:
            recommendations.append(f"虚拟机内存({memory_mb}MB)过大，"
                                 f"建议调整为{self.recommended_settings['recommended_memory_mb']}MB")
        
        # 检查磁盘配置
        disk_size_gb = self._get_disk_size_gb(vm_config.get('disk_path', ''))
        recommended_disk = self.recommended_settings['recommended_disk_size_gb']
        if disk_size_gb and disk_size_gb > recommended_disk * 2:
            recommendations.append(f"虚拟机磁盘容量较大，建议根据实际需要调整")
        
        return recommendations if recommendations else ["虚拟机配置合理，性能表现良好"]
    
    def _get_disk_size_gb(self, disk_path: str) -> Optional[float]:
        """获取磁盘文件大小(GB)"""
        try:
            if disk_path and Path(disk_path).exists():
                size_bytes = Path(disk_path).stat().st_size
                return size_bytes / (1024**3)
        except:
            pass
        return None


# 全局性能优化器实例
performance_optimizer = PerformanceOptimizer()


def get_performance_optimizer() -> PerformanceOptimizer:
    """获取性能优化器实例"""
    global performance_optimizer
    return performance_optimizer