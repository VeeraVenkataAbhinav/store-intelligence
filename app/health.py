import json
import os
from datetime import datetime
from app.logger import logger

EVENT_FILE = "events/events.jsonl"


def health_status():

    last_timestamp = None

    if os.path.exists(EVENT_FILE):

        with open(EVENT_FILE, "r") as f:

            for line in f:

                try:
                    event = json.loads(line)

                    ts = event.get(
                        "timestamp"
                    )

                    if ts:
                        last_timestamp = ts

                except:
                    continue

    stale_feed = False

    if last_timestamp:

        try:
            last_dt = datetime.fromisoformat(
                last_timestamp.replace(
                    "Z",
                    ""
                )
            )

            now = datetime.utcnow()

            lag = (
                now - last_dt
            ).total_seconds()

            if lag > 600:
                stale_feed = True

        except Exception as e:
             logger.error(f"Health error: {e}")

    return {
        "service": "healthy",
        "last_event_timestamp": last_timestamp,
        "stale_feed": stale_feed
    }