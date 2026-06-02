import json
import os
import csv

EVENT_FILE = "events/events.jsonl"
POS_FILE = "pos_transactions.csv"


def compute_conversion(store_id):

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

    # Entry visitors
    entry_visitors = set()

    for e in events:

        if e.get(
            "event_type"
        ) == "ENTRY":

            entry_visitors.add(
                e.get(
                    "visitor_id"
                )
            )

    total_entries = len(
        entry_visitors
    )

    # POS transactions
    purchase_count = 0

    if os.path.exists(POS_FILE):

        with open(
            POS_FILE,
            newline=""
        ) as csvfile:

            reader = csv.DictReader(
                csvfile
            )

            for row in reader:
                purchase_count += 1

    conversion_rate = 0

    if total_entries > 0:

        conversion_rate = round(
            (
                purchase_count
                / total_entries
            )
            * 100,
            2
        )

    return {
        "store_id": store_id,
        "entries": total_entries,
        "purchases": purchase_count,
        "conversion_rate": conversion_rate
    }