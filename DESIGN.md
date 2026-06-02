# DESIGN.md

# Smart Retail Intelligence System Design

## System Overview

The Smart Retail Intelligence System converts raw anonymized CCTV footage into real-time retail analytics.

The architecture follows an event-driven pipeline where camera detections are transformed into structured visitor behavior events and exposed through a FastAPI intelligence layer.

The system was designed around the challenge North Star metric:

Offline Store Conversion Rate

Conversion Rate = Converted Visitors / Total Unique Visitors


## Architecture Flow

Raw CCTV Clips
        ↓
YOLOv8 Detection + Tracking
        ↓
Zone / Queue / Entry Logic
        ↓
Structured Event Emission
        ↓
JSONL Event Storage
        ↓
FastAPI Analytics Layer
        ↓
Metrics / Funnel / Health / Conversion / Dashboard


## Detection Layer

YOLOv8 was used for person detection.

Tracking is performed using YOLO persistent tracking IDs.

Three camera workflows were implemented:

CAM1:

Zone monitoring.

Generates:

- ZONE_ENTER
- ZONE_DWELL
- ZONE_EXIT

CAM3:

Entry and exit monitoring.

Generates:

- ENTRY
- EXIT
- REENTRY

Threshold-crossing logic is used to determine visitor movement direction.

CAM5:

Billing queue monitoring.

Uses ROI rectangle logic to:

- count queue depth
- generate queue alerts
- monitor crowd buildup


## Event Pipeline

Each behavioral event is emitted through emit.py.

Events contain:

- event_id
- visitor_id
- camera_id
- event_type
- timestamp
- dwell_ms
- confidence
- metadata

Events are stored in JSONL format and later ingested by the API layer.


## Intelligence Layer

FastAPI exposes analytics endpoints.

Implemented APIs:

- /health
- /metrics
- /funnel
- /anomalies
- /conversion

The API computes real-time store intelligence from emitted events and POS transactions.


## AI-Assisted Decisions

AI tools were used as engineering accelerators rather than code generators.

AI assistance influenced several parts of the system:

1. Detection pipeline debugging and event-flow validation.

AI suggestions were used to improve camera-specific logic and troubleshoot runtime issues.

2. Queue intelligence implementation.

AI-assisted reasoning helped refine billing queue ROI tuning and alert thresholds.

3. Documentation and architecture presentation.

AI was used to improve readability and structure of README and design documentation.

However, implementation choices and final logic decisions were manually verified and adapted during development.


## Tradeoffs

Several tradeoffs were made.

YOLOv8 tracking IDs were used rather than a heavier Re-ID model to balance implementation speed and computational simplicity.

JSONL storage was selected instead of a database for lightweight real-time experimentation.

Queue logic was implemented using geometric ROI regions rather than segmentation to keep runtime fast and interpretable.


## Future Improvements

Potential improvements include:

- Deep Re-ID models
- Cross-camera identity matching
- Advanced queue abandonment prediction
- Database-backed event storage
- Multi-store scaling