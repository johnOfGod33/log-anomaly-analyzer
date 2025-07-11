import asyncio
import json

from models.event import Event
from models.event_analyzer import EventAnalyzer
from models.event_logger import EventLogger


async def read_logs(file):
    with open(file, "r") as f:
        event_logger = EventLogger()
        event_analyzer = EventAnalyzer()
        cpt = 0

        for line in f:
            line = line.strip()

            if line == "":
                continue

            cpt += 1

            event_json = json.loads(line)

            event = create_event(event_json)

            event_analyzer.add_event(event)

            event_logger.log_event(event)

            if event_analyzer.detect_alerts():
                event_analyzer.save_alert()

            await asyncio.sleep(2)

        return event_analyzer, event_logger


def create_event(event_json: dict):
    event_id = event_json["event_id"]
    event_type = event_json["level"]
    timestamp = event_json["timestamp"]
    message = event_json["message"]
    return Event(
        event_id=event_id,
        event_type=event_type,
        timestamp=timestamp,
        message=message,
    )


def show_alerts(event_analyzer: EventAnalyzer, event_logger: EventLogger):
    alerts = event_analyzer.alerts
    event_logger.log_alerts(alerts)


def generate_report(event_analyzer: EventAnalyzer):
    with open("alerts.json", "w") as f:
        json.dump(event_analyzer.alerts, f)

    event_analyzer.generate_histogram()
    event_analyzer.write_report()
