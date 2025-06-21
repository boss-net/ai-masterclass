import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


@dataclass
class Message:
    type: "MessageType"
    source: str
    target: str
    data: Dict[str, Any]
    timestamp: float

    def to_json(self) -> str:
        """Convert message to JSON string."""
        return json.dumps(
            {
                "type": self.type.value,
                "source": self.source,
                "target": self.target,
                "data": self.data,
                "timestamp": self.timestamp,
            }
        )

    @classmethod
    def from_json(cls, json_str: str) -> "Message":
        """Create message from JSON string."""
        data = json.loads(json_str)
        return cls(
            type=MessageType(data["type"]),
            source=data["source"],
            target=data["target"],
            data=data["data"],
            timestamp=data["timestamp"],
        )


class MessageType(Enum):
    METRIC = "METRIC"
    ALERT = "ALERT"
    CONFIG = "CONFIG"
    STATUS = "STATUS"
    HEARTBEAT = "HEARTBEAT"
    JOIN = "JOIN"
    LEAVE = "LEAVE"
    QUERY = "QUERY"
    RESPONSE = "RESPONSE"
