import json
import os
from app.logger import logger

EVENT_FILE = "events/events.jsonl"


def compute_funnel(store_id):

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
                 logger.error(f"Funnel error: {e}")
                continue

    entry_visitors = set()
    queue_visitors = set()
    purchase_visitors = set()

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
            continue

        if is_staff:
            continue

        visitor = e.get(
            "visitor_id"
        )

        etype = e.get(
            "event_type"
        )

        if etype == "ENTRY":
            entry_visitors.add(visitor)

        elif etype == "BILLING_QUEUE_JOIN":
            queue_visitors.add(visitor)

        elif etype == "PURCHASE":
            purchase_visitors.add(visitor)

    return {
        "store_id": store_id,
        "entries": len(entry_visitors),
        "billing_queue": len(queue_visitors),
        "purchases": len(purchase_visitors)
    }