import logging
import socket
import threading
import time
from typing import Any, Dict

from monitoring.collector import MetricCollector
from monitoring.monitor import Monitor

from .message import Message, MessageType

logger = logging.getLogger(__name__)


class MonitoringNode:
    def __init__(self, node_id: str, coordinator_host: str, coordinator_port: int):
        self.node_id = node_id
        self.coordinator_host = coordinator_host
        self.coordinator_port = coordinator_port

        self.monitor = Monitor()
        self.collector = MetricCollector()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False

        # Thread for sending metrics
        self.send_thread = None

        # Thread for receiving messages
        self.recv_thread = None

    def start(self):
        """Start the monitoring node."""
        try:
            # Connect to coordinator
            self.sock.connect((self.coordinator_host, self.coordinator_port))

            # Send join message
            self._send_message(
                Message(
                    type=MessageType.JOIN,
                    source=self.node_id,
                    target="coordinator",
                    data={"node_id": self.node_id},
                    timestamp=time.time(),
                )
            )

            # Start threads
            self.running = True
            self.send_thread = threading.Thread(target=self._send_metrics)
            self.recv_thread = threading.Thread(target=self._receive_messages)

            self.send_thread.start()
            self.recv_thread.start()

            logger.info(f"Node {self.node_id} started")

        except Exception as e:
            logger.error(f"Failed to start node: {e}")
            raise

    def stop(self):
        """Stop the monitoring node."""
        self.running = False
        if self.send_thread:
            self.send_thread.join()
        if self.recv_thread:
            self.recv_thread.join()
        self.sock.close()
        logger.info(f"Node {self.node_id} stopped")

    def _send_metrics(self):
        """Send metrics to coordinator."""
        while self.running:
            try:
                # Collect metrics
                metrics = self.collector.collect_all()

                # Send metrics
                self._send_message(
                    Message(
                        type=MessageType.METRIC,
                        source=self.node_id,
                        target="coordinator",
                        data={"metrics": metrics},
                        timestamp=time.time(),
                    )
                )

                # Send heartbeat
                self._send_message(
                    Message(
                        type=MessageType.HEARTBEAT,
                        source=self.node_id,
                        target="coordinator",
                        data={},
                        timestamp=time.time(),
                    )
                )

                time.sleep(5)  # Send interval

            except Exception as e:
                logger.error(f"Error sending metrics: {e}")
                time.sleep(1)  # Retry interval

    def _receive_messages(self):
        """Receive messages from coordinator."""
        while self.running:
            try:
                # Receive message
                data = self.sock.recv(4096)
                if not data:
                    break

                # Process message
                message = Message.from_json(data.decode())
                self._process_message(message)

            except Exception as e:
                logger.error(f"Error receiving message: {e}")
                time.sleep(1)

    def _process_message(self, message: Message):
        """Process incoming message."""
        if message.type == MessageType.CONFIG:
            self._handle_config(message)
        elif message.type == MessageType.QUERY:
            self._handle_query(message)
        elif message.type == MessageType.ALERT:
            self._handle_alert(message)

    def _handle_config(self, message: Message):
        """Handle configuration update."""
        config = message.data.get("config", {})
        self.monitor.update_config(config)
        self.collector.update_config(config)

    def _handle_query(self, message: Message):
        """Handle query from coordinator."""
        query = message.data.get("query", {})
        result = self.monitor.get_metrics(**query)

        self._send_message(
            Message(
                type=MessageType.RESPONSE,
                source=self.node_id,
                target=message.source,
                data={"result": result},
                timestamp=time.time(),
            )
        )

    def _handle_alert(self, message: Message):
        """Handle alert from coordinator."""
        alert = message.data.get("alert", {})
        self.monitor.add_alert(alert)

    def _send_message(self, message: Message):
        """Send message to coordinator."""
        self.sock.sendall(message.to_json().encode())
