# -*- coding: utf-8 -*-
"""
网络管理器
用于管理虚拟机网络配置、端口转发等功能
"""

import subprocess
import socket
import ipaddress
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import platform


@dataclass
class NetworkInterface:
    """网络接口数据类"""
    name: str
    ip_address: str
    subnet_mask: str
    mac_address: str
    status: str  # up, down


@dataclass
class PortForwardingRule:
    """端口转发规则数据类"""
    protocol: str  # tcp, udp
    host_port: int
    guest_ip: str
    guest_port: int
    description: str = ""


class NetworkManager:
    """网络管理器"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.interfaces = self._get_network_interfaces()
    
    def _get_network_interfaces(self) -> List[NetworkInterface]:
        """获取系统网络接口信息"""
        interfaces = []
        try:
            if self.system == "linux":
                # Linux 系统获取网络接口信息
                import netifaces
                for interface in netifaces.interfaces():
                    addrs = netifaces.ifaddresses(interface)
                    if netifaces.AF_INET in addrs:
                        ipv4_info = addrs[netifaces.AF_INET][0]
                        ip_addr = ipv4_info['addr']
                        netmask = ipv4_info.get('netmask', '')
                        
                        # 获取接口状态
                        is_up = interface in netifaces.interfaces()
                        status = "up" if is_up else "down"
                        
                        # MAC地址
                        mac_addr = ""
                        if netifaces.AF_LINK in addrs:
                            mac_addr = addrs[netifaces.AF_LINK][0].get('addr', '')
                        
                        interfaces.append(NetworkInterface(
                            name=interface,
                            ip_address=ip_addr,
                            subnet_mask=netmask,
                            mac_address=mac_addr,
                            status=status
                        ))
            elif self.system == "windows":
                # Windows 系统获取网络接口信息
                import wmi
                c = wmi.WMI()
                for adapter in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
                    if adapter.IPAddress:
                        ip_addr = adapter.IPAddress[0]
                        netmask = adapter.IPSubnet[0] if adapter.IPSubnet else ""
                        mac_addr = adapter.MACAddress or ""
                        status = "up" if adapter.IPEnabled else "down"
                        
                        interfaces.append(NetworkInterface(
                            name=adapter.Description,
                            ip_address=ip_addr,
                            subnet_mask=netmask,
                            mac_address=mac_addr,
                            status=status
                        ))
            else:
                # 其他系统，返回基本信息
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                
                interfaces.append(NetworkInterface(
                    name="default",
                    ip_address=local_ip,
                    subnet_mask="255.255.255.0",
                    mac_address="",
                    status="up"
                ))
        except ImportError:
            # 如果没有netifaces或wmi库，返回基本网络信息
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname) if platform.system() != "Darwin" else "127.0.0.1"
            
            interfaces.append(NetworkInterface(
                name="default",
                ip_address=local_ip,
                subnet_mask="255.255.255.0",
                mac_address="",
                status="up"
            ))
        
        return interfaces
    
    def get_available_network_modes(self) -> List[str]:
        """获取可用的网络模式"""
        modes = ["用户模式 (User/NAT)", "桥接模式 (Bridge)", "仅主机模式 (Host-only)"]
        
        # 检查是否支持特定网络模式
        if self.system == "linux":
            # 检查是否安装了bridge-utils
            try:
                subprocess.run(['which', 'brctl'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                # 桥接模式可用
                pass
            except subprocess.CalledProcessError:
                # 桥接模式不可用
                pass
        
        return modes
    
    def get_host_ip_addresses(self) -> List[str]:
        """获取主机IP地址列表"""
        return [iface.ip_address for iface in self.interfaces if iface.status == "up"]
    
    def check_port_availability(self, port: int) -> bool:
        """检查端口是否可用"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return True
        except OSError:
            return False
    
    def get_available_port(self, start_port: int = 5900) -> int:
        """获取可用端口"""
        port = start_port
        while not self.check_port_availability(port):
            port += 1
        return port
    
    def create_port_forwarding_command(self, protocol: str, host_port: int, guest_ip: str, guest_port: int) -> List[str]:
        """创建端口转发命令参数"""
        # 为QEMU创建端口转发参数
        if protocol.lower() == 'tcp':
            return ['-netdev', f'user,id=net0,hostfwd={protocol.lower()}::{host_port}-:{guest_port}']
        else:
            return ['-netdev', f'user,id=net0,hostfwd={protocol.lower()}::{host_port}-:{guest_port}']
    
    def validate_ip_address(self, ip: str) -> bool:
        """验证IP地址格式"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def validate_port_range(self, port: int) -> bool:
        """验证端口范围"""
        return 1 <= port <= 65535
    
    def get_network_stats(self) -> Dict:
        """获取网络统计信息"""
        stats = {
            'interfaces': len(self.interfaces),
            'active_interfaces': len([iface for iface in self.interfaces if iface.status == 'up']),
            'host_ips': self.get_host_ip_addresses(),
            'available_modes': self.get_available_network_modes()
        }
        
        return stats
    
    def configure_vm_network(self, vm_name: str, network_mode: str = "user", 
                           bridge_interface: str = "", mac_address: str = "") -> List[str]:
        """配置虚拟机网络参数"""
        # 根据网络模式生成QEMU网络参数
        network_params = []
        
        if network_mode == "用户模式 (User/NAT)":
            network_params.extend([
                "-netdev", "user,id=net0",
                "-device", "virtio-net-pci,netdev=net0"
            ])
        elif network_mode == "桥接模式 (Bridge)":
            if bridge_interface:
                network_params.extend([
                    "-netdev", f"bridge,id=net0,br={bridge_interface}",
                    "-device", "virtio-net-pci,netdev=net0"
                ])
        elif network_mode == "仅主机模式 (Host-only)":
            network_params.extend([
                "-netdev", "user,id=net0",
                "-device", "virtio-net-pci,netdev=net0"
            ])
        
        # 如果指定了MAC地址
        if mac_address:
            # 在现有网络设备参数中添加MAC地址
            for i, param in enumerate(network_params):
                if "virtio-net-pci" in param:
                    # 修改网络设备参数以包含MAC地址
                    if ",mac=" not in param:
                        network_params[i] = param.replace(",netdev=", f",mac={mac_address},netdev=")
        
        return network_params


# 全局网络管理器实例
network_manager = NetworkManager()


def get_network_manager() -> NetworkManager:
    """获取网络管理器实例"""
    global network_manager
    return network_manager