from datetime import time, timedelta

from .event import Event


class EventAnalyzer:
    def __init__(self):
        self.events: list[Event] = []
        self.alerts: list[dict] = []

    def add_event(self, event: Event):
        self.events.append(event)

    def detect_alerts(self):
        events = self.get_last_events()

        if len(events) < 3:
            return False

        start_time = events[0].get_event_datetime()
        end_time = events[-1].get_event_datetime()
        interval = end_time - start_time
        is_critical = True

        for event in events:
            if not event.is_critical():
                is_critical = False
                break

        return is_critical and interval < timedelta(seconds=30)

    def get_last_events(self):
        return self.events[-3:]

    def save_alert(self):
        events = self.get_last_events()
        alert = {
            "alert_id": len(self.alerts) + 1,
            "events": [event.to_dict() for event in events],
        }
        self.alerts.append(alert)
