from datetime import datetime


class Event:
    def __init__(self, event_id: str, event_type: str, timestamp: str, message: str):
        self.event_id = event_id
        self.event_type = event_type
        self.timestamp = timestamp
        self.message = message

    def is_critical(self):
        return self.event_type == "ERROR" or self.event_type == "CRITICAL"

    def get_event_datetime(self):
        """Convert timestamp string to datetime object"""
        return datetime.fromisoformat(self.timestamp.replace("Z", "+00:00"))
