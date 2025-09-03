import psutil
import platform
import datetime
from typing import Dict, Any
from cynetics.tools.base import BaseTool

class SystemMonitorTool(BaseTool):
    """A tool for monitoring system resources and performance."""
    
    def __init__(self):
        super().__init__(
            name="system_monitor",
            description="Monitor system resources including CPU, memory, disk, and network usage."
        )
    
    def run(self, action: str = "full", duration: int = 1) -> Dict[str, Any]:
        """Monitor system resources.
        
        Args:
            action: Type of monitoring ('full', 'cpu', 'memory', 'disk', 'network', 'processes')
            duration: Duration to monitor for (seconds, for CPU usage)
            
        Returns:
            A dictionary with system monitoring information.
        """
        try:
            if action == "full":
                return self._get_full_system_info()
            elif action == "cpu":
                return self._get_cpu_info(duration)
            elif action == "memory":
                return self._get_memory_info()
            elif action == "disk":
                return self._get_disk_info()
            elif action == "network":
                return self._get_network_info()
            elif action == "processes":
                return self._get_process_info()
            else:
                return {
                    "status": "error",
                    "message": f"Unknown action: {action}"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _get_full_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information."""
        return {
            "status": "success",
            "action": "full",
            "timestamp": datetime.datetime.now().isoformat(),
            "system": self._get_system_info(),
            "cpu": self._get_cpu_info(),
            "memory": self._get_memory_info(),
            "disk": self._get_disk_info(),
            "network": self._get_network_info(),
            "processes": self._get_process_info()
        }
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get basic system information."""
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "platform_release": platform.release(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        }
    
    def _get_cpu_info(self, duration: int = 1) -> Dict[str, Any]:
        """Get CPU information."""
        return {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "max_frequency": psutil.cpu_freq().max if psutil.cpu_freq() else None,
            "min_frequency": psutil.cpu_freq().min if psutil.cpu_freq() else None,
            "current_frequency": psutil.cpu_freq().current if psutil.cpu_freq() else None,
            "cpu_usage_per_core": [percentage for percentage in psutil.cpu_percent(percpu=True, interval=duration)],
            "total_cpu_usage": psutil.cpu_percent(interval=duration)
        }
    
    def _get_memory_info(self) -> Dict[str, Any]:
        """Get memory information."""
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            "total_memory": svmem.total,
            "available_memory": svmem.available,
            "used_memory": svmem.used,
            "percentage_memory": svmem.percent,
            "swap_total": swap.total,
            "swap_used": swap.used,
            "swap_free": swap.free,
            "swap_percentage": swap.percent
        }
    
    def _get_disk_info(self) -> Dict[str, Any]:
        """Get disk information."""
        partitions = psutil.disk_partitions()
        disk_info = []
        
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "file_system": partition.fstype,
                    "total_size": partition_usage.total,
                    "used": partition_usage.used,
                    "free": partition_usage.free,
                    "percentage": partition_usage.percent
                })
            except PermissionError:
                # Handle cases where permission is denied
                continue
        
        return {
            "partitions": disk_info,
            "total_read": psutil.disk_io_counters().read_bytes if psutil.disk_io_counters() else None,
            "total_write": psutil.disk_io_counters().write_bytes if psutil.disk_io_counters() else None
        }
    
    def _get_network_info(self) -> Dict[str, Any]:
        """Get network information."""
        if_addrs = psutil.net_if_addrs()
        net_info = {}
        
        for interface_name, interface_addresses in if_addrs.items():
            addresses = []
            for address in interface_addresses:
                addresses.append({
                    "family": str(address.family),
                    "address": address.address,
                    "netmask": address.netmask,
                    "broadcast": address.broadcast
                })
            net_info[interface_name] = addresses
        
        net_io = psutil.net_io_counters()
        
        return {
            "interfaces": net_info,
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }
    
    def _get_process_info(self, top_n: int = 5) -> Dict[str, Any]:
        """Get process information."""
        processes = []
        
        # Get all processes
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                # Get process info
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Sort by CPU usage and get top N
        processes.sort(key=lambda x: x['cpu_percent'] if x['cpu_percent'] is not None else 0, reverse=True)
        
        return {
            "total_processes": len(processes),
            "top_cpu_processes": processes[:top_n],
            "top_memory_processes": sorted(processes, 
                                         key=lambda x: x['memory_percent'] if x['memory_percent'] is not None else 0, 
                                         reverse=True)[:top_n]
        }