import json
import os

EVENT_FILE = "events/events.jsonl"


def compute_heatmap(store_id):

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

                except:
                    continue

    zone_counts = {}

    for e in events:

        zone = e.get(
            "zone_id"
        )

        if zone is None:
            zone = "UNKNOWN"

        zone_counts[zone] = (
            zone_counts.get(zone, 0)
            + 1
        )

    return {
        "store_id": store_id,
        "zones": zone_counts
    }