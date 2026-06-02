# Smart Retail Intelligence System

AI-powered offline retail analytics system built for Purplle Tech Challenge 2026.

This system processes anonymized CCTV footage using YOLO-based detection and tracking, generates structured behavioral events, and exposes a FastAPI-based intelligence layer for real-time retail analytics.

The pipeline supports:

- Entry / Exit detection
- Re-entry handling
- Zone monitoring
- Billing queue detection
- Queue alerts
- Visitor conversion analytics
- Funnel analysis
- Health monitoring
- Operational anomaly detection

North Star Metric:

Offline Store Conversion Rate

Conversion Rate = Converted Visitors / Total Unique Visitors


## Architecture

Raw CCTV Clips
        ↓
YOLOv8 Detection + Tracking
        ↓
Behavior Event Emission
        ↓
Event Storage (JSONL)
        ↓
FastAPI Intelligence Layer
        ↓
Metrics / Funnel / Anomalies / Conversion / Dashboard


## Project Structure

store-intelligence/
├── pipeline/
│   ├── detect.py
│   ├── emit.py
│   └── zone_tracker.py
├── app/
│   ├── main.py
│   ├── ingestion.py
│   ├── metrics.py
│   ├── funnel.py
│   ├── anomalies.py
│   ├── conversion.py
│   └── health.py
├── events/
├── Dockerfile
├── requirements.txt
└── README.md

## Installation

Clone repository:

git clone <repo-url>

Create virtual environment:

python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt


## Running the Backend

Start FastAPI server:

uvicorn app.main:app --reload

Backend runs at:

http://127.0.0.1:8000


## Running Detection Pipeline

Open:

pipeline/detect.py

Choose camera:

CAM1:

VIDEO_PATH = "CAM 1.mp4"

CAM3:

VIDEO_PATH = "CAM 3.mp4"

CAM5:

VIDEO_PATH = "CAM 5.mp4"

Run:

python pipeline\detect.py


## Camera Logic

### CAM1 – Zone Monitoring

Tracks visitors inside LEFT_ZONE and emits:

- ZONE_ENTER
- ZONE_DWELL
- ZONE_EXIT


### CAM3 – Entry / Exit / Re-entry

Uses threshold crossing logic.

Events:

- ENTRY
- EXIT
- REENTRY

Re-entry logic prevents duplicate visitor sessions.


### CAM5 – Billing Queue

Billing queue region monitored using ROI rectangle.

Features:

- Queue count
- Queue alert
- Queue monitoring
- Crowd build-up detection


## API Endpoints

Health:

/health

Metrics:

/stores/STORE_BLR_002/metrics

Funnel:

/stores/STORE_BLR_002/funnel

Anomalies:

/stores/STORE_BLR_002/anomalies

Conversion:

/stores/STORE_BLR_002/conversion


## Live Dashboard

Dashboard available at:

http://127.0.0.1:8000/

Displays:

- Event log
- Queue count
- Queue alert
- Visitor statistics