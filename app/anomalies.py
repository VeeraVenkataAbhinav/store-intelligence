import json
import os

EVENT_FILE = "events/events.jsonl"
QUEUE_FILE = "events/queue.json"


def detect_anomalies(store_id):

    anomalies = []

    # Queue anomaly
    if os.path.exists(QUEUE_FILE):

        with open(QUEUE_FILE, "r") as f:

            queue_data = json.load(f)

            if queue_data.get(
                "alert",
                False
            ):

                anomalies.append(
                    {
                        "type": "LONG_QUEUE",
                        "severity": "HIGH"
                    }
                )

    # Traffic anomaly
    event_count = 0

    if os.path.exists(EVENT_FILE):

        with open(EVENT_FILE, "r") as f:

            for line in f:

                try:
                    event = json.loads(line)

                    if (
                        event.get("store_id")
                        == store_id
                    ):
                        event_count += 1

                except:
                    continue

    if event_count > 100:

        anomalies.append(
            {
                "type": "HIGH_TRAFFIC",
                "severity": "MEDIUM"
            }
        )

    return {
        "store_id": store_id,
        "anomalies": anomalies
    }