import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class Dashboard:
    def __init__(self, title: str):
        self.title = title
        self.charts = []
        self.metrics = []
        self.alerts = []

    def add_chart(self, chart):  # Removed type hint to avoid undefined 'Chart'
        """Add a chart to the dashboard."""
        self.charts.append(chart)

    def add_metric(self, metric: Dict[str, Any]):
        """Add a metric to the dashboard."""
        self.metrics.append(metric)

    def add_alert(self, alert: Dict[str, Any]):
        """Add an alert to the dashboard."""
        self.alerts.append(alert)

    def generate(self, format: str = "html") -> str:
        """Generate the dashboard in specified format."""
        if format == "html":
            return self._generate_html()
        elif format == "pdf":
            return self._generate_pdf()
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _generate_html(self) -> str:
        """Generate HTML dashboard."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{self.title}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <h1>{self.title}</h1>
            <div id="dashboard">
        """

        # Add charts
        for i, chart in enumerate(self.charts):
            html += f"<div id='chart{i}'></div>"
            html += f"<script>var plot{i} = {chart.to_json()}; " f"Plotly.newPlot('chart{i}', plot{i});</script>"

        # Add metrics
        html += "<h2>Metrics</h2>"
        html += "<div class='metrics'>"
        for metric in self.metrics:
            html += "<div class='metric'>"
            html += f"<h3>{metric['name']}</h3>"
            html += f"<p>Value: {metric['value']}</p>"
            html += f"<p>Timestamp: {metric['timestamp']}</p>"
            html += "</div>"
        html += "</div>"

        # Add alerts
        html += "<h2>Alerts</h2>"
        html += "<div class='alerts'>"
        for alert in self.alerts:
            html += f"<div class='alert {alert['level']}'>"
            html += f"<h3>{alert['level'].upper()} Alert</h3>"
            html += f"<p>Metric: {alert['metric']}</p>"
            html += f"<p>Value: {alert['value']}</p>"
            html += f"<p>Timestamp: {alert['timestamp']}</p>"
            html += "</div>"
        html += "</div>"

        html += "</div></body></html>"
        return html

    def _generate_pdf(self) -> str:
        """Generate PDF dashboard."""
        # Implementation for PDF generation
        raise NotImplementedError("PDF generation not implemented yet")
