import json
import logging
import sqlite3
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class AlertHistory:
    def __init__(self, db_path: str = "alerts.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Initialize the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    level TEXT NOT NULL,
                    metric TEXT NOT NULL,
                    value REAL NOT NULL,
                    source TEXT NOT NULL,
                    nodes TEXT,
                    resolved BOOLEAN DEFAULT FALSE,
                    resolution_timestamp TEXT
                )
            """
            )
            conn.commit()

    def add_alert(self, alert: Dict[str, Any]):
        """Add an alert to history."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO alerts (
                    timestamp, level, metric, value, source, nodes
                ) VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    alert["timestamp"],
                    alert["level"],
                    alert["metric"],
                    alert["value"],
                    alert["source"],
                    json.dumps(alert.get("nodes", [])),
                ),
            )
            conn.commit()

    def resolve_alert(self, alert_id: int):
        """Mark an alert as resolved."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE alerts SET
                    resolved = TRUE,
                    resolution_timestamp = ?
                WHERE id = ?
            """,
                (datetime.now().isoformat(), alert_id),
            )
            conn.commit()

    def get_alerts(
        self,
        level: str = None,
        metric: str = None,
        source: str = None,
        resolved: bool = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get alerts from history."""
        query = "SELECT * FROM alerts WHERE 1=1"
        params = []

        if level:
            query += " AND level = ?"
            params.append(level)

        if metric:
            query += " AND metric = ?"
            params.append(metric)

        if source:
            query += " AND source = ?"
            params.append(source)

        if resolved is not None:
            query += " AND resolved = ?"
            params.append(resolved)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            return [
                {
                    "id": row[0],
                    "timestamp": row[1],
                    "level": row[2],
                    "metric": row[3],
                    "value": row[4],
                    "source": row[5],
                    "nodes": json.loads(row[6]),
                    "resolved": bool(row[7]),
                    "resolution_timestamp": row[8],
                }
                for row in rows
            ]

    def get_alert_stats(self) -> Dict[str, Any]:
        """Get alert statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT level, COUNT(*) as count
                FROM alerts
                GROUP BY level
            """
            )
            level_stats = dict(cursor.fetchall())

            cursor.execute(
                """
                SELECT metric, COUNT(*) as count
                FROM alerts
                GROUP BY metric
            """
            )
            metric_stats = dict(cursor.fetchall())

            cursor.execute(
                """
                SELECT COUNT(*) as total, SUM(CASE WHEN resolved = 1 THEN 1 ELSE 0 END) as resolved
                FROM alerts
            """
            )
            total_stats = cursor.fetchone()

            return {
                "total_alerts": total_stats[0],
                "resolved_alerts": total_stats[1],
                "level_stats": level_stats,
                "metric_stats": metric_stats,
            }
