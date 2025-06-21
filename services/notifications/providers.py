import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict

import requests

logger = logging.getLogger(__name__)


class EmailProvider:
    def __init__(
        self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send(self, alert: Dict[str, Any]) -> bool:
        """Send email notification."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = alert.get("recipient_email", self.sender_email)
            msg["Subject"] = f"{alert['level'].upper()} Alert: {alert['metric']}"

            # Create body
            body = f"""
            Alert: {alert['level'].upper()}
            Metric: {alert['metric']}
            Value: {alert['value']}
            Timestamp: {alert['timestamp']}
            """

            msg.attach(MIMEText(body, "plain"))

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False


class SlackProvider:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, alert: Dict[str, Any]) -> bool:
        """Send Slack notification."""
        try:
            # Create message
            payload = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{alert['level'].upper()} Alert: {alert['metric']}*",
                        },
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Value:*\n{alert['value']}"},
                            {
                                "type": "mrkdwn",
                                "text": f"*Timestamp:*\n{alert['timestamp']}",
                            },
                        ],
                    },
                ]
            }

            # Send message
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to send Slack message: {e}")
            return False


class WebhookProvider:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, alert: Dict[str, Any]) -> bool:
        """Send webhook notification."""
        try:
            # Send webhook
            response = requests.post(
                self.webhook_url,
                json=alert,
                headers={"Content-Type": "application/json"},
            )

            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to send webhook: {e}")
            return False
