from flask import Flask, jsonify, send_from_directory
from datetime import datetime
import psutil
import os

# Get the absolute path of the website folder (parent of this file's "api" folder)
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Create Flask application
app = Flask(__name__)


# ==============================
# ANOMALY DETECTION THRESHOLDS
# ------------------------------
# Current implementation: simple rule/threshold-based detection.
# This is intentionally NOT machine learning - it is a fast, transparent
# baseline. A trained model (see /models/isolation_forest.joblib) can be
# swapped in later behind the same evaluate_metric()/build_metrics_payload()
# interface without changing the API contract below.
# ==============================
THRESHOLDS = {
    "cpu": {"warning": 70, "anomaly": 85},
    "memory": {"warning": 75, "anomaly": 90},
    "disk": {"warning": 80, "anomaly": 90},
}


def evaluate_metric(name, usage_percent):
    """Rule-based status classification for a single metric."""
    limits = THRESHOLDS[name]
    if usage_percent >= limits["anomaly"]:
        return "anomaly"
    if usage_percent >= limits["warning"]:
        return "warning"
    return "normal"


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


# ==============================
# STATIC ASSETS (CSS / JS)
# ==============================

@app.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory(ASSETS_DIR, filename)


# ==============================
# HEALTH CHECK
# ==============================

@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


# ==============================
# SERVER METRICS
# ==============================

@app.route("/api/metrics")
def metrics():

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    cpu_status = evaluate_metric("cpu", cpu)
    memory_status = evaluate_metric("memory", memory.percent)
    disk_status = evaluate_metric("disk", disk.percent)

    statuses = [cpu_status, memory_status, disk_status]
    if "anomaly" in statuses:
        overall_status = "anomaly"
    elif "warning" in statuses:
        overall_status = "warning"
    else:
        overall_status = "normal"

    return jsonify({
        "cpu": {
            "usage_percent": cpu,
            "status": cpu_status
        },

        "memory": {
            "usage_percent": memory.percent,
            "total": memory.total,
            "used": memory.used,
            "status": memory_status
        },

        "disk": {
            "usage_percent": disk.percent,
            "total": disk.total,
            "used": disk.used,
            "status": disk_status
        },

        "overall_status": overall_status,
        "detection_method": "rule_based_threshold",
        "timestamp": datetime.now().isoformat()
    })


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5001)