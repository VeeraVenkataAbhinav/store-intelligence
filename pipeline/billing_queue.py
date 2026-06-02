from ultralytics import YOLO
import cv2
import json
from emit import emit_event

# Load model
model = YOLO("yolov8n.pt")

# Open CAM5
cap = cv2.VideoCapture("CAM 5.mp4")

ALERT_THRESHOLD = 2

# Queue zone
x1, y1 = 0, 220
x2, y2 = 520, 540

# Track queue joins
queued_ids = set()

while cap.isOpened():

    success, frame = cap.read()

    if not success:
        break

    results = model(
        frame,
        classes=[0],
        conf=0.5
    )

    annotated_frame = frame.copy()

    queue_count = 0

    # Draw queue zone
    cv2.rectangle(
        annotated_frame,
        (x1, y1),
        (x2, y2),
        (0, 255, 255),
        3
    )

    if results[0].boxes is not None:

        for i, box in enumerate(results[0].boxes):

            x_min, y_min, x_max, y_max = map(
                int,
                box.xyxy[0]
            )

            cx = (x_min + x_max) // 2
            cy = (y_min + y_max) // 2

            if x1 < cx < x2 and y1 < cy < y2:

                queue_count += 1

                cv2.rectangle(
                    annotated_frame,
                    (x_min, y_min),
                    (x_max, y_max),
                    (255, 0, 0),
                    2
                )

                cv2.putText(
                    annotated_frame,
                    "person",
                    (x_min, y_min - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 0, 0),
                    2
                )

                # Queue Join Event
                if i not in queued_ids:

                    queued_ids.add(i)

                    emit_event(
                        store_id="STORE_BLR_002",
                        camera_id="CAM_BILLING_01",
                        visitor_id=str(i),
                        event_type="BILLING_QUEUE_JOIN",
                        confidence=0.90,
                        zone_id="QUEUE_ZONE_01",
                        metadata={
                            "queue_depth": queue_count
                        }
                    )

                    print(
                        "QUEUE JOIN",
                        i
                    )

    # Save queue data
    with open("events/queue.json", "w") as f:

        json.dump(
            {
                "queue_count": queue_count,
                "alert": queue_count >= ALERT_THRESHOLD
            },
            f
        )

    # Queue count
    cv2.putText(
        annotated_frame,
        f"Queue Count: {queue_count}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    # Alert
    if queue_count >= ALERT_THRESHOLD:

        cv2.putText(
            annotated_frame,
            "ALERT: Long Queue!",
            (20, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            3
        )

    cv2.imshow(
        "Billing Queue Zone",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()