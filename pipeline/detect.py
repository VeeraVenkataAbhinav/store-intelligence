from ultralytics import YOLO
import cv2
from emit import emit_event
from zone_tracker import update_zone, reset_zones

# Load model
model = YOLO("yolov8n.pt")

# Select camera
VIDEO_PATH = "CAM 5.mp4"

reset_zones()

cap = cv2.VideoCapture(VIDEO_PATH)

LINE_X1, LINE_Y1 = 900, 750
LINE_X2, LINE_Y2 = 1350, 250

track_last_side = {}
recent_exits = {}

while cap.isOpened():

    success, frame = cap.read()

    if not success:
        break

    results = model.track(
        frame,
        persist=True,
        classes=[0],
        conf=0.5
    )

    annotated_frame = results[0].plot()

    if results[0].boxes.id is not None:

        boxes = results[0].boxes.xyxy.cpu().numpy()
        track_ids = results[0].boxes.id.cpu().numpy()

        for box, track_id in zip(boxes, track_ids):

            print(
                "TRACK LOOP RUNNING",
                track_id
            )

            x1, y1, x2, y2 = map(int, box)

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

                        # CAM1
            if "CAM 1" in VIDEO_PATH:

                zone_event, dwell = update_zone(
                    str(track_id),
                    "LEFT_ZONE"
                )

                if zone_event is not None:

                    emit_event(
                        str(track_id),
                        zone_event,
                        "CAM_LEFT_01",
                        zone_id="LEFT_ZONE",
                        dwell_ms=dwell
                    )

            # CAM2
            elif "CAM 2" in VIDEO_PATH:

                zone_event, dwell = update_zone(
                    str(track_id),
                    "RIGHT_ZONE"
                )

                if zone_event is not None:

                    emit_event(
                        str(track_id),
                        zone_event,
                        "CAM_RIGHT_01",
                        zone_id="RIGHT_ZONE",
                        dwell_ms=dwell
                    )

            # CAM3
            elif "CAM 3" in VIDEO_PATH:

                line_y = LINE_Y1 + (
                    (LINE_Y2 - LINE_Y1)
                    * (cx - LINE_X1)
                    / (LINE_X2 - LINE_X1)
                )

                current_side = (
                    "below"
                    if cy > line_y
                    else "above"
                )

                if track_id in track_last_side:

                    prev_side = track_last_side[
                        track_id
                    ]

                    # ENTRY / REENTRY
                    if (
                        prev_side == "above"
                        and current_side == "below"
                    ):

                        if str(track_id) in recent_exits:

                            emit_event(
                                str(track_id),
                                "REENTRY",
                                "CAM_ENTRY_01"
                            )

                            print(
                                "REENTRY",
                                track_id
                            )

                            del recent_exits[
                                str(track_id)
                            ]

                        else:

                            emit_event(
                                str(track_id),
                                "ENTRY",
                                "CAM_ENTRY_01"
                            )

                            print(
                                "ENTRY",
                                track_id
                            )

                    # EXIT
                    elif (
                        prev_side == "below"
                        and current_side == "above"
                    ):

                        emit_event(
                            str(track_id),
                            "EXIT",
                            "CAM_ENTRY_01"
                        )

                        print(
                            "EXIT",
                            track_id
                        )

                        recent_exits[
                            str(track_id)
                        ] = True

                track_last_side[
                    track_id
                ] = current_side

    cv2.circle(
                annotated_frame,
                (cx, cy),
                5,
                (0, 0, 255),
                -1
            )

    # CAM3 entry line
    if "CAM 3" in VIDEO_PATH:

        cv2.line(
            annotated_frame,
            (LINE_X1, LINE_Y1),
            (LINE_X2, LINE_Y2),
            (0, 255, 0),
            4
        )

    # CAM5 queue zone
    # CAM5 queue zone
    if "CAM 5" in VIDEO_PATH and results[0].boxes.id is not None:

        queue_count = 0

        # Yellow rectangle
        cv2.rectangle(
            annotated_frame,
            (50, 220),
            (550, 540),
            (0, 255, 255),
            3
        )

        # Count people inside rectangle
        for box in boxes:

            x1, y1, x2, y2 = map(int, box)

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            if (
                20 < cx < 750
                and
                140 < cy < 400
            ):
                queue_count += 1

        # Queue count (RED)
        cv2.putText(
            annotated_frame,
            f"QUEUE: {queue_count}",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        # Queue alert
        if queue_count >= 3:

            cv2.putText(
                annotated_frame,
                "QUEUE ALERT",
                (250, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

    cv2.imshow(
        "Detection",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()