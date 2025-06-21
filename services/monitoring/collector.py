import logging
import time
from datetime import datetime
from typing import Any, Dict

import psutil

logger = logging.getLogger(__name__)


class MetricCollector:
    def __init__(self, interval: int = 1):
        self.interval = interval
        self.metrics = []

    def collect_cpu(self) -> Dict[str, Any]:
        """Collect CPU metrics."""
        return {
            "percent": psutil.cpu_percent(),
            "count": psutil.cpu_count(),
            "timestamp": datetime.now().isoformat(),
        }

    def collect_memory(self) -> Dict[str, Any]:
        """Collect memory metrics."""
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
            "timestamp": datetime.now().isoformat(),
        }

    def collect_disk(self) -> Dict[str, Any]:
        """Collect disk metrics."""
        disk_usage = psutil.disk_usage("/")
        return {
            "total": disk_usage.total,
            "used": disk_usage.used,
            "free": disk_usage.free,
            "percent": disk_usage.percent,
            "timestamp": datetime.now().isoformat(),
        }

    def collect_network(self) -> Dict[str, Any]:
        """Collect network metrics."""
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "timestamp": datetime.now().isoformat(),
        }

    def collect_all(self) -> Dict[str, Any]:
        """Collect all metrics."""
        return {
            "cpu": self.collect_cpu(),
            "memory": self.collect_memory(),
            "disk": self.collect_disk(),
            "network": self.collect_network(),
            "timestamp": datetime.now().isoformat(),
        }

    def start_collection(self, duration: int = None):
        """Start continuous metric collection."""
        start_time = time.time()

        while True:
            current_time = time.time()
            if duration and current_time - start_time >= duration:
                break

            metrics = self.collect_all()
            self.metrics.append(metrics)

            time.sleep(self.interval)

    def get_metrics(self) -> list:
        """Get collected metrics."""
        return self.metrics

    def reset(self):
        """Reset collected metrics."""
        self.metrics = []
