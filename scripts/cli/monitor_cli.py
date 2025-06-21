import json
import logging
from datetime import datetime

import click
from monitoring.collector import MetricCollector
from monitoring.monitor import AlertThreshold, Monitor
from notifications.notifier import Notifier
from notifications.providers import EmailProvider, SlackProvider

from visualization.dashboard import Dashboard

logger = logging.getLogger(__name__)


class MonitorCLI:
    def __init__(self):
        self.monitor = Monitor()
        self.collector = MetricCollector()
        self.notifier = Notifier()

        # Set up default thresholds
        self._setup_thresholds()

        # Set up default providers
        self._setup_providers()

    def _setup_thresholds(self):
        """Set up default alert thresholds."""
        self.monitor.add_threshold(
            AlertThreshold(
                metric="cpu.percent",
                operator=">",
                value=90,
                duration=60,
                alert_level="critical",
            )
        )

        self.monitor.add_threshold(
            AlertThreshold(
                metric="memory.rss",
                operator=">",
                value=8589934592,  # 8GB
                duration=60,
                alert_level="warning",
            )
        )

    def _setup_providers(self):
        """Set up default notification providers."""
        # Email provider
        try:
            with open("config/email.json") as f:
                email_config = json.load(f)
            email_provider = EmailProvider(**email_config)
            self.notifier.add_provider(email_provider)
        except Exception as e:
            logger.warning(f"Failed to set up email provider: {e}")

        # Slack provider
        try:
            with open("config/slack.json") as f:
                slack_config = json.load(f)
            slack_provider = SlackProvider(**slack_config)
            self.notifier.add_provider(slack_provider)
        except Exception as e:
            logger.warning(f"Failed to set up Slack provider: {e}")

    @click.command()
    @click.option("--duration", default=60, help="Monitoring duration in seconds")
    @click.option("--interval", default=5, help="Metric collection interval in seconds")
    @click.option("--output", default="html", help="Output format (html, json)")
    def start(self, duration: int, interval: int, output: str):
        """Start monitoring system."""
        # Start metric collection
        self.collector.interval = interval
        self.collector.start_collection(duration)

        # Process metrics
        while True:
            metrics = self.collector.get_metrics()
            for metric in metrics:
                self.monitor.add_metric(metric)

            # Generate dashboard
            dashboard = self._generate_dashboard()

            # Save dashboard
            if output == "html":
                with open(
                    f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html", "w"
                ) as f:
                    f.write(dashboard.generate("html"))
            elif output == "json":
                with open(
                    f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w"
                ) as f:
                    json.dump(dashboard.metrics, f, indent=2)

            # Check for alerts
            alerts = self.monitor.get_alerts()
            if alerts:
                self._handle_alerts(alerts)

            # Exit if duration is reached
            if duration and time.time() - start_time >= duration:
                break

    def _generate_dashboard(self) -> Dashboard:
        """Generate dashboard with current metrics."""
        dashboard = Dashboard("AI Masterclass Monitoring")

        # Add charts
        dashboard.add_chart(
            LineChart(
                title="CPU Usage", data=self.collector.get_metrics(name="cpu.percent")
            )
        )

        dashboard.add_chart(
            BarChart(
                title="Memory Usage", data=self.collector.get_metrics(name="memory.rss")
            )
        )

        # Add metrics
        for metric in self.collector.get_metrics():
            dashboard.add_metric(metric)

        # Add alerts
        for alert in self.monitor.get_alerts():
            dashboard.add_alert(alert)

        return dashboard

    def _handle_alerts(self, alerts: list):
        """Handle and notify about alerts."""
        for alert in alerts:
            logger.warning(f"Alert: {alert}")
            self.notifier.notify(alert)


# Create CLI command
def main():
    cli = MonitorCLI()
    cli.start()


if __name__ == "__main__":
    main()
