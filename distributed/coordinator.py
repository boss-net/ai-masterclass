import logging
import socket
import threading
import time
from typing import Any, Dict, List

from monitoring.monitor import Monitor
from notifications.notifier import Notifier

from .message import Message, MessageType

logger = logging.getLogger(__name__)


class MonitoringCoordinator:
    def __init__(self, host: str = "0.0.0.0", port: int = 9000):
        self.host = host
        self.port = port

        self.monitor = Monitor()
        self.notifier = Notifier()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

        self.nodes = {}  # node_id -> connection
        self.running = False

        # Thread for handling connections
        self.conn_thread = None

        # Thread for processing alerts
        self.alert_thread = None

    def start(self):
        """Start the coordinator."""
        try:
            self.sock.listen()

            # Start threads
            self.running = True
            self.conn_thread = threading.Thread(target=self._handle_connections)
            self.alert_thread = threading.Thread(target=self._process_alerts)

            self.conn_thread.start()
            self.alert_thread.start()

            logger.info(f"Coordinator started on {self.host}:{self.port}")

        except Exception as e:
            logger.error(f"Failed to start coordinator: {e}")
            raise

    def stop(self):
        """Stop the coordinator."""
        self.running = False
        if self.conn_thread:
            self.conn_thread.join()
        if self.alert_thread:
            self.alert_thread.join()
        self.sock.close()
        logger.info("Coordinator stopped")

    def _handle_connections(self):
        """Handle incoming connections."""
        while self.running:
            try:
                conn, addr = self.sock.accept()
                logger.info(f"Connection from {addr}")

                # Handle connection in new thread
                threading.Thread(target=self._handle_client, args=(conn, addr)).start()

            except Exception as e:
                logger.error(f"Error handling connection: {e}")
                time.sleep(1)

    def _handle_client(self, conn, addr):
        """Handle client connection."""
        while self.running:
            try:
                data = conn.recv(4096)
                if not data:
                    break

                # Process message
                message = Message.from_json(data.decode())
                self._process_message(message, conn)

            except Exception as e:
                logger.error(f"Error handling client: {e}")
                break

        conn.close()

    def _process_message(self, message: Message, conn):
        """Process incoming message."""
        if message.type == MessageType.JOIN:
            self._handle_join(message, conn)
        elif message.type == MessageType.LEAVE:
            self._handle_leave(message)
        elif message.type == MessageType.METRIC:
            self._handle_metrics(message)
        elif message.type == MessageType.HEARTBEAT:
            self._handle_heartbeat(message)
        elif message.type == MessageType.QUERY:
            self._handle_query(message, conn)

    def _handle_join(self, message: Message, conn):
        """Handle node join."""
        node_id = message.data.get("node_id")
        self.nodes[node_id] = conn
        logger.info(f"Node {node_id} joined")

    def _handle_leave(self, message: Message):
        """Handle node leave."""
        node_id = message.source
        if node_id in self.nodes:
            del self.nodes[node_id]
            logger.info(f"Node {node_id} left")

    def _handle_metrics(self, message: Message):
        """Handle incoming metrics."""
        metrics = message.data.get("metrics", [])
        for metric in metrics:
            self.monitor.add_metric(metric)

    def _handle_heartbeat(self, message: Message):
        """Handle heartbeat."""
        node_id = message.source
        if node_id in self.nodes:
            self.nodes[node_id].last_heartbeat = time.time()

    def _handle_query(self, message: Message, conn):
        """Handle query from node."""
        query = message.data.get("query", {})
        result = self.monitor.get_metrics(**query)

        response = Message(
            type=MessageType.RESPONSE,
            source="coordinator",
            target=message.source,
            data={"result": result},
            timestamp=time.time(),
        )

        conn.sendall(response.to_json().encode())

    def _process_alerts(self):
        """Process alerts from nodes."""
        while self.running:
            try:
                # Check for alerts
                alerts = self.monitor.get_alerts()
                if alerts:
                    # Aggregate alerts
                    aggregated = self._aggregate_alerts(alerts)

                    # Notify
                    self.notifier.notify(aggregated)

                # Clean up stale nodes
                self._cleanup_nodes()

                time.sleep(5)  # Process interval

            except Exception as e:
                logger.error(f"Error processing alerts: {e}")
                time.sleep(1)

    def _aggregate_alerts(self, alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aggregate alerts from multiple nodes."""
        aggregated = {}

        for alert in alerts:
            key = f"{alert['metric']}_{alert['level']}"
            if key not in aggregated:
                aggregated[key] = {**alert, "nodes": set()}
            aggregated[key]["nodes"].add(alert["source"])

        return [
            {**alert, "nodes": list(alert["nodes"])} for alert in aggregated.values()
        ]

    def _cleanup_nodes(self):
        """Clean up stale nodes."""
        current_time = time.time()
        stale_threshold = 60  # 60 seconds

        for node_id, conn in list(self.nodes.items()):
            if hasattr(conn, "last_heartbeat"):
                if current_time - conn.last_heartbeat > stale_threshold:
                    del self.nodes[node_id]
                    logger.info(f"Node {node_id} marked as stale")
