import json
import os
from app.logger import logger

EVENT_FILE = "events/events.jsonl"


def compute_metrics(store_id):

    events = []

    if os.path.exists(EVENT_FILE):

        with open(EVENT_FILE, "r") as f:

            for line in f:

                try:
                    event = json.loads(line)

                    if (
                        event.get("store_id")
                        == store_id
                    ):
                        events.append(event)

                except Exception as e:
                  logger.error(f"Metrics error: {e}")
                continue

    # Unique visitors
    visitors = set()

    for e in events:

        is_staff = e.get(
            "is_staff",
            False
        )

        camera = e.get(
            "camera_id",
            ""
        )

        if "STAFF" in camera:
            is_staff = True

        if not is_staff:

            visitors.add(
                e.get(
                    "visitor_id"
                )
            )

    unique_visitors = len(
        visitors
    )

    # Queue depth
    queue_events = [

        e for e in events

        if e.get(
            "event_type"
        )
        == "BILLING_QUEUE_JOIN"
    ]

    queue_depth = len(
        queue_events
    )

    return {
        "store_id": store_id,
        "unique_visitors": unique_visitors,
        "queue_depth": queue_depth,
        "conversion_rate": 0
    }