import logging
import time
from typing import Any, Dict

import psutil

logger = logging.getLogger(__name__)


class MetricsCollector:
    def __init__(self):
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss

    def collect(self) -> Dict[str, Any]:
        """Collect various performance metrics."""
        return {
            "cpu": self._get_cpu_metrics(),
            "memory": self._get_memory_metrics(),
            "disk": self._get_disk_metrics(),
            "network": self._get_network_metrics(),
        }

    def _get_cpu_metrics(self) -> Dict[str, Any]:
        """Get CPU metrics."""
        cpu_percent = psutil.cpu_percent()
        cpu_count = psutil.cpu_count()
        return {"percent": cpu_percent, "count": cpu_count}

    def _get_memory_metrics(self) -> Dict[str, Any]:
        """Get memory metrics."""
        process = psutil.Process()
        mem_info = process.memory_info()
        return {
            "rss": mem_info.rss,
            "vms": mem_info.vms,
            "shared": mem_info.shared,
            "text": mem_info.text,
            "lib": mem_info.lib,
            "data": mem_info.data,
            "dirty": mem_info.dirty,
        }

    def _get_disk_metrics(self) -> Dict[str, Any]:
        """Get disk metrics."""
        disk_usage = psutil.disk_usage("/")
        return {
            "total": disk_usage.total,
            "used": disk_usage.used,
            "free": disk_usage.free,
            "percent": disk_usage.percent,
        }

    def _get_network_metrics(self) -> Dict[str, Any]:
        """Get network metrics."""
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
        }

    def reset(self):
        """Reset metrics collection."""
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss
