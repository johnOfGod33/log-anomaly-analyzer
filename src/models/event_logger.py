import logging

from models.event import Event


class EventLogger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        self.logger = logging.getLogger(__name__)

    def log_event(self, event: Event):
        message = f"Événement traité : [{event.event_type}] - {event.timestamp} - {event.message}"
        self.logger.info(message)
