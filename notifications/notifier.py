import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class NotificationProvider(ABC):
    @abstractmethod
    def send(self, alert: Dict[str, Any]) -> bool:
        """Send an alert notification."""
        pass


class Notifier:
    def __init__(self):
        self.providers = []
        self.alerts = []

    def add_provider(self, provider: NotificationProvider):
        """Add a notification provider."""
        self.providers.append(provider)

    def notify(self, alert: Dict[str, Any]) -> List[bool]:
        """Send notification to all providers."""
        results = []
        for provider in self.providers:
            try:
                success = provider.send(alert)
                results.append(success)
                if not success:
                    logger.error(
                        f"Failed to send notification via {provider.__class__.__name__}"
                    )
            except Exception as e:
                logger.error(f"Error sending notification: {e}")
                results.append(False)
        return results

    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get all alerts."""
        return self.alerts

    def clear_alerts(self):
        """Clear all alerts."""
        self.alerts = []
