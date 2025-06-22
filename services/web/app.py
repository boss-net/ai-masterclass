import logging

from flask import Flask, jsonify, request  # type: ignore
from monitoring.alert_history import AlertHistory
from monitoring.monitor import Monitor
from visualization.dashboard import Dashboard

logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

    # Initialize components
    app.monitor = Monitor()
    app.alert_history = AlertHistory()

    # Register routes
    @app.route("/api/metrics", methods=["GET"])
    def get_metrics():
        """Get current metrics."""
        metrics = app.monitor.get_metrics()
        return jsonify(metrics)

    @app.route("/api/alerts", methods=["GET"])
    def get_alerts():
        """Get alerts from history."""
        level = request.args.get("level")
        metric = request.args.get("metric")
        source = request.args.get("source")
        resolved = request.args.get("resolved")

        alerts = app.alert_history.get_alerts(level=level, metric=metric, source=source, resolved=resolved)
        return jsonify(alerts)

    @app.route("/api/alerts/stats", methods=["GET"])
    def get_alert_stats():
        """Get alert statistics."""
        stats = app.alert_history.get_alert_stats()
        return jsonify(stats)

    @app.route("/api/dashboard", methods=["GET"])
    def get_dashboard():
        """Get dashboard HTML."""
        dashboard = Dashboard("AI Masterclass Monitoring")

        # Add metrics
        metrics = app.monitor.get_metrics()
        for metric in metrics:
            dashboard.add_metric(metric)

        # Add alerts
        alerts = app.alert_history.get_alerts(limit=10)
        for alert in alerts:
            dashboard.add_alert(alert)

        return dashboard.generate("html")

    @app.route("/api/config", methods=["GET", "POST"])
    def config():
        """Get or update configuration."""
        if request.method == "POST":
            config = request.json
            app.monitor.update_config(config)
            return jsonify({"status": "success"})

        return jsonify(app.monitor.get_config())

    return app
