import json
import uuid
from datetime import datetime


def emit_event(
    visitor_id,
    event_type,
    camera_id,
    zone_id=None,
    dwell_ms=0,
    queue_depth=None
):

    event = {

        "event_id": str(
            uuid.uuid4()
        ),

        "store_id":
        "STORE_BLR_002",

        "camera_id":
        camera_id,

        "visitor_id":
        f"VIS_{visitor_id}",

        "event_type":
        event_type,

        "timestamp":
        datetime.utcnow()
        .isoformat()
        + "Z",

        "zone_id":
        zone_id,

        "dwell_ms":
        dwell_ms,

        "is_staff":
        False,

        "confidence":
        0.90,

        "metadata": {

            "queue_depth":
            queue_depth,

            "session_seq":
            1
        }
    }

    print(
        "EVENT:",
        event
    )

    with open(
        "events/events.jsonl",
        "a"
    ) as f:

        f.write(
            json.dumps(
                event
            )
            + "\n"
        )