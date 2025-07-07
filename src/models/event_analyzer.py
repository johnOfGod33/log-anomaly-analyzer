import json
from collections import Counter
from datetime import timedelta

import matplotlib.pyplot as plt
from fpdf import FPDF

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

        return is_critical and interval <= timedelta(seconds=30)

    def get_last_events(self):
        return self.events[-3:]

    def save_alert(self):
        events = self.get_last_events()
        alert = {
            "alert_id": len(self.alerts) + 1,
            "timestamp": events[-1].timestamp,
            "events": [event.to_dict() for event in events],
        }
        self.alerts.append(alert)

    def generate_histogram(self, filename="histogram.png"):
        levels = [event.event_type for event in self.events]
        level_counts = Counter(levels)

        plt.figure(figsize=(8, 5))
        plt.bar(level_counts.keys(), level_counts.values(), color="blue")
        plt.title("Event Frequency by Level")
        plt.xlabel("Level")
        plt.ylabel("Frequency")
        plt.savefig(filename)
        plt.close()

    def write_report(self, filename="report.pdf", histogram_file="histogram.png"):
        total_events = len(self.events)
        critical_events = len([event for event in self.events if event.is_critical()])
        total_alerts = len(self.alerts)
        alerts_timestamps = [alert["timestamp"] for alert in self.alerts]

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "==== End of Processing Report ====", ln=True)
        pdf.cell(0, 10, f"Total number of events: {total_events}", ln=True)
        pdf.cell(0, 10, f"Number of critical events: {critical_events}", ln=True)
        pdf.cell(0, 10, f"Number of alerts: {total_alerts}", ln=True)
        pdf.cell(0, 10, "Alert timestamps:", ln=True)
        for ts in alerts_timestamps:
            pdf.cell(0, 10, f"  - {ts}", ln=True)
        pdf.ln(10)
        pdf.cell(0, 10, "Event Frequency Histogram:", ln=True)
        pdf.image(histogram_file, x=10, w=pdf.w - 20)
        pdf.output(filename)
