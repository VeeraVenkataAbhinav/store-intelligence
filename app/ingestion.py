import json
import os
from app.logger import logger

EVENT_FILE = "events/events.jsonl"


def ingest_events(events):

    stored_ids = set()

    # Load existing event IDs
    if os.path.exists(EVENT_FILE):

        with open(EVENT_FILE, "r") as f:

            for line in f:

                try:
                    event = json.loads(line)

                    if "event_id" in event:
                        stored_ids.add(
                            event["event_id"]
                        )

                except Exception as e:
                 logger.error(f"Ingestion error: {e}")
                continue

    results = []

    with open(EVENT_FILE, "a") as f:

        for event in events:

            event_id = event.get(
                "event_id"
            )

            if event_id in stored_ids:

                results.append(
                    {
                        "event_id": event_id,
                        "status": "duplicate"
                    }
                )

            else:

                f.write(
                    json.dumps(event)
                    + "\n"
                )

                stored_ids.add(
                    event_id
                )

                results.append(
                    {
                        "event_id": event_id,
                        "status": "stored"
                    }
                )

    return results