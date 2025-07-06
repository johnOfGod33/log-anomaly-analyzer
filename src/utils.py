import asyncio
import json

from models.event import Event
from models.event_logger import EventLogger


async def read_logs(file):
    event_logger = EventLogger()
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            event_json = json.loads(line)
            event = create_event(event_json)
            event_logger.log_event(event)
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
