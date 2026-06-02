import time

zone_memory = {}


def reset_zones():
    global zone_memory
    zone_memory = {}


def update_zone(
    track_id,
    zone_name
):

    now = time.time()

    # FIRST ENTRY
    if track_id not in zone_memory:

        print(
            "FIRST ENTRY",
            track_id
        )

        zone_memory[
            track_id
        ] = {
            "zone": zone_name,
            "start": now
        }

        return "ZONE_ENTER", 0

    start_time = zone_memory[
        track_id
    ]["start"]

    dwell_ms = int(
        (now - start_time)
        * 1000
    )

    # Dwell every 10 sec
    if dwell_ms >= 10000:

        zone_memory[
            track_id
        ]["start"] = now

        return "ZONE_DWELL", dwell_ms

    return None, dwell_ms