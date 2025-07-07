import json
from collections import Counter
from datetime import datetime, timedelta

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
            "start_timestamp": events[0].timestamp,
            "end_timestamp": events[-1].timestamp,
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

        pdf = FPDF()
        pdf.add_page()

        # Title
        pdf.set_font("Arial", "B", 18)
        pdf.set_text_color(30, 30, 120)
        pdf.cell(0, 15, "Logs Report", ln=True, align="C")
        pdf.set_draw_color(30, 30, 120)
        pdf.set_line_width(0.8)
        pdf.line(10, 28, 200, 28)
        pdf.ln(10)

        # Section: Summary
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Summary", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, f"Total number of events: {total_events}", ln=True)
        pdf.cell(0, 8, f"Number of critical events: {critical_events}", ln=True)
        pdf.cell(0, 8, f"Number of alerts: {total_alerts}", ln=True)
        pdf.ln(5)

        # Section: Alerts Table
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Alert Details", ln=True)
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(30, 8, "Alert ID", border=1, fill=True, align="C")
        pdf.cell(70, 8, "Start Timestamp", border=1, fill=True, align="C")
        pdf.cell(70, 8, "End Timestamp", border=1, fill=True, align="C")
        pdf.ln()
        pdf.set_font("Arial", "", 12)
        for alert in self.alerts:
            pdf.cell(30, 8, str(alert["alert_id"]), border=1, align="C")
            pdf.cell(70, 8, alert["start_timestamp"], border=1, align="C")
            pdf.cell(70, 8, alert["end_timestamp"], border=1, align="C")
            pdf.ln()
        pdf.ln(8)

        # Section: Histogram
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Event Frequency Histogram", ln=True)
        pdf.image(histogram_file, x=30, w=pdf.w - 60)
        pdf.ln(10)

        pdf.output(filename)
