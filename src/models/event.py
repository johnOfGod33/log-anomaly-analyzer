class Event:
    def __init__(self, event_id, event_type, timestamp, message):
        self.event_id = event_id
        self.event_type = event_type
        self.timestamp = timestamp
        self.message = message

    def is_critical(self):
        return self.event_type == "ERROR" or self.event_type == "CRITICAL"
