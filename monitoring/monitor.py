import logging
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict

logger = logging.getLogger(__name__)


@dataclass
class Metric:
    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str] = None


@dataclass
class AlertThreshold:
    metric: str
    operator: str
    value: float
    duration: int  # seconds
    alert_level: str = "warning"

    def check(self, metric: Metric) -> bool:
        """Check if metric violates threshold."""
        if self.operator == "<":
            return metric.value < self.value
        elif self.operator == ">":
            return metric.value > self.value
        elif self.operator == "==":
            return metric.value == self.value
        return False


class Monitor:
    def __init__(self):
        self.metrics = []
        self.alerts = []
        self.thresholds = []
        self.collector = MetricCollector()

    def add_metric(self, metric: Metric):
        """Add a new metric."""
        self.metrics.append(metric)
        self._check_thresholds(metric)

    def add_threshold(self, threshold: AlertThreshold):
        """Add a new alert threshold."""
        self.thresholds.append(threshold)

    def _check_thresholds(self, metric: Metric):
        """Check if metric violates any thresholds."""
        for threshold in self.thresholds:
            if threshold.metric == metric.name:
                if threshold.check(metric):
                    self._create_alert(metric, threshold)

    def _create_alert(self, metric: Metric, threshold: AlertThreshold):
        """Create an alert for a violated threshold."""
        alert = {
            "metric": metric.name,
            "value": metric.value,
            "threshold": threshold.value,
            "operator": threshold.operator,
            "level": threshold.alert_level,
            "timestamp": datetime.now().isoformat(),
        }
        self.alerts.append(alert)
        logger.warning(f"Alert created: {alert}")

    def get_metrics(self, name: str = None, tags: Dict[str, str] = None) -> list:
        """Get metrics by name and tags."""
        if name and tags:
            return [
                m
                for m in self.metrics
                if m.name == name and all(m.tags.get(k) == v for k, v in tags.items())
            ]
        elif name:
            return [m for m in self.metrics if m.name == name]
        elif tags:
            return [
                m
                for m in self.metrics
                if all(m.tags.get(k) == v for k, v in tags.items())
            ]
        return self.metrics

    def get_alerts(self, level: str = None) -> list:
        """Get alerts by level."""
        if level:
            return [a for a in self.alerts if a["level"] == level]
        return self.alerts
