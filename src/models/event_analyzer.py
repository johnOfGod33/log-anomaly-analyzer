from .event import Event


class EventAnalyzer:
    def __init__(self):
        self.events: list[Event] = []
        self.alerts: list[Event] = []

    def add_event(self, event: Event):
        self.events.append(event)

    def detect_alerts(self):
        pass
