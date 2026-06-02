from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import os
from app.ingestion import ingest_events
from app.metrics import compute_metrics
from app.health import health_status
from app.funnel import compute_funnel
from app.heatmap import compute_heatmap
from app.anomalies import detect_anomalies
from app.conversion import compute_conversion
from app.logger import logger
from fastapi import Body

app = FastAPI()


# Dashboard
@app.get("/", response_class=HTMLResponse)
def dashboard():
    logger.info("Dashboard opened")

    events = []

    try:
        with open("events/events.jsonl", "r") as f:
            for line in f:
                events.append(json.loads(line))
    except:
        pass

    entry_count = sum(
        1 for e in events
        if e["event_type"] == "ENTRY"
    )

    # Queue data
    queue_count = 0
    alert = False

    if os.path.exists("events/queue.json"):
        with open("events/queue.json", "r") as f:
            queue_data = json.load(f)
            queue_count = queue_data["queue_count"]
            alert = queue_data["alert"]

    alert_text = "YES" if alert else "NO"

    return f"""
<html>
<head>
<title>Smart Retail Intelligence</title>

<style>

body {{
    margin:0;
    font-family:Segoe UI;
    background:#0f172a;
    color:white;
    padding:40px;
}}

h1 {{
    text-align:center;
    font-size:42px;
    margin-bottom:10px;
}}

.subtitle {{
    text-align:center;
    color:#cbd5e1;
    margin-bottom:35px;
}}

.container {{
    display:flex;
    gap:25px;
    flex-wrap:wrap;
    justify-content:center;
}}

.card {{
    width:280px;
    padding:25px;
    border-radius:20px;
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(10px);
    box-shadow:0 8px 25px rgba(255,255,255,0.08);
    transition:0.3s;
}}

.card:hover {{
    transform:translateY(-5px);
}}

.entries {{
    border-left:6px solid #ffffff;
}}

.queue {{
    border-left:6px solid #10b981;
}}

.alertyes {{
    border-left:6px solid #ef4444;
}}

.alertno {{
    border-left:6px solid #22c55e;
}}

.number {{
    font-size:42px;
    font-weight:bold;
}}

.label {{
    color:#e2e8f0;
    margin-top:8px;
    font-size:18px;
}}

.log {{
    margin-top:35px;
    background:#111827;
    padding:20px;
    border-radius:18px;
    box-shadow:0 8px 20px rgba(255,255,255,0.05);
}}

pre {{
    color:#22c55e;
    overflow-x:auto;
}}

</style>
</head>

<body>

<h1>🤍 Smart Retail Intelligence</h1>

<div class="subtitle">
Live AI Monitoring Dashboard
</div>

<div class="container">

    <div class="card entries">
        <div class="number">{entry_count}</div>
        <div class="label">Total Entries</div>
    </div>

    <div class="card queue">
        <div class="number">{queue_count}</div>
        <div class="label">Queue Count</div>
    </div>

    <div class="card {'alertyes' if alert else 'alertno'}">
        <div class="number">{alert_text}</div>
        <div class="label">Queue Alert</div>
    </div>

</div>

<div class="log">
<h3>📜 Event Log</h3>
<pre>{json.dumps(events, indent=2)}</pre>
</div>

</body>
</html>
"""


# Events API
@app.get("/events")
def get_events():
    logger.info("Events API called")
    events = []

    try:
        with open("events/events.jsonl", "r") as f:
            for line in f:
                events.append(json.loads(line))
    except:
        pass

    return events


# Stats API
@app.get("/stats")
def get_stats():
    events = []

    try:
        with open("events/events.jsonl", "r") as f:
            for line in f:
                events.append(json.loads(line))
    except:
        pass

    entry_count = sum(
        1 for e in events
        if e["event_type"] == "ENTRY"
    )

    return {
        "total_entries": entry_count
    }


# Queue API
@app.get("/queue")
def get_queue():

    if os.path.exists("events/queue.json"):
        with open("events/queue.json", "r") as f:
            return json.load(f)

    return {
        "queue_count": 0,
        "alert": False
    }
# Event Ingest API
@app.post("/events/ingest")
def events_ingest(
    events: list = Body(...)
):

    result = ingest_events(
        events
    )

    return {
        "results": result
    }
# Store Metrics API
@app.get("/stores/{store_id}/metrics")
def store_metrics(
    store_id: str
):

    logger.info(f"Metrics requested for {store_id}")

    return compute_metrics(
        store_id
    )
# Health API
@app.get("/health")
def health():
    logger.info("Health check called")
    return health_status()
# Funnel API
@app.get("/stores/{store_id}/funnel")
def funnel(
    store_id: str
):

    return compute_funnel(
        store_id
    )
# Heatmap API
@app.get("/stores/{store_id}/heatmap")
def heatmap(
    store_id: str
):

    return compute_heatmap(
        store_id
    )
# Anomalies API
@app.get("/stores/{store_id}/anomalies")
def anomalies(
    store_id: str
):

    return detect_anomalies(
        store_id
    )
# Conversion API
@app.get("/stores/{store_id}/conversion")
def conversion(
    store_id: str
):

    logger.info(f"Conversion requested for {store_id}")

    return compute_conversion(
        store_id
    )