import json
import logging

from models.event import Event


class EventLogger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        self.logger = logging.getLogger(__name__)

    def log_event(self, event: Event):
        message = f"Processed event: [{event.event_type}] - {event.timestamp} - {event.message}"
        self.logger.info(message)

    def log_alerts(self, alerts: list[dict]):
        if not alerts:
            logging.info("No alerts detected.")
            return

        logging.info(f"=== {len(alerts)} ALERT(S) DETECTED ===")

        for alert in alerts:
            alert_msg = (
                f"ALERT #{alert['alert_id']}: "
                f"3 critical events between {alert['start_timestamp']} "
                f"and {alert['end_timestamp']} "
            )
            logging.warning(alert_msg)
