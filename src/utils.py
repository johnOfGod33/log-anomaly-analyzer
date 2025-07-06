import asyncio
import json

from models.event import Event
from models.event_analyzer import EventAnalyzer
from models.event_logger import EventLogger


async def read_logs(file):
    event_logger = EventLogger()
    event_analyzer = EventAnalyzer()

    with open(file, "r") as f:
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

            if cpt % 3 == 0:
                if event_analyzer.detect_alerts():
                    event_logger.log_alert()

            await asyncio.sleep(2)


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
