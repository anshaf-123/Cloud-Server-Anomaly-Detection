/*
 * Cloud Server Anomaly Detection - Dashboard Frontend Logic
 * Fetches real metrics from /api/metrics (relative URL - works on
 * whichever host/port Flask is actually running on, no hardcoding).
 */

function setStatusClass(el, status) {
    el.classList.remove("status-normal", "status-warning", "status-danger");
    if (status === "anomaly") {
        el.classList.add("status-danger");
    } else if (status === "warning") {
        el.classList.add("status-warning");
    } else {
        el.classList.add("status-normal");
    }
}

function updateOverallStatus(status) {
    const heading = document.getElementById("overall-status");
    const text = document.getElementById("overall-status-text");
    const dot = document.getElementById("overall-status-dot");

    const labels = {
        normal: "HEALTHY",
        warning: "WARNING",
        anomaly: "ANOMALY DETECTED"
    };

    heading.textContent = labels[status] || "UNKNOWN";
    setStatusClass(heading, status);
    setStatusClass(dot, status);

    if (status === "anomaly") {
        text.textContent = "One or more metrics exceeded critical thresholds";
    } else if (status === "warning") {
        text.textContent = "Some metrics are elevated - monitor closely";
    } else {
        text.textContent = "All systems operational";
    }
}

function updateAnomalyPanel(status) {
    const icon = document.getElementById("anomaly-icon");
    const heading = document.getElementById("anomaly-heading");
    const text = document.getElementById("anomaly-text");

    if (status === "anomaly") {
        icon.textContent = "🚨";
        heading.textContent = "Anomaly Detected";
        text.textContent = "One or more server metrics have exceeded the configured anomaly threshold. Investigate immediately.";
    } else if (status === "warning") {
        icon.textContent = "⚠️";
        heading.textContent = "Elevated Usage";
        text.textContent = "One or more metrics are approaching threshold limits.";
    } else {
        icon.textContent = "🛡️";
        heading.textContent = "No Critical Anomalies";
        text.textContent = "Your server metrics are currently within normal operating ranges.";
    }
}

async function loadMetrics() {
    try {
        const response = await fetch("/api/metrics");

        if (!response.ok) {
            throw new Error("HTTP " + response.status);
        }

        const data = await response.json();

        // CPU
        document.getElementById("cpu").textContent = data.cpu.usage_percent.toFixed(1) + "%";
        document.getElementById("cpu-progress").style.width = data.cpu.usage_percent + "%";

        // Memory
        document.getElementById("memory").textContent = data.memory.usage_percent.toFixed(1) + "%";
        document.getElementById("memory-progress").style.width = data.memory.usage_percent + "%";

        // Disk
        document.getElementById("disk").textContent = data.disk.usage_percent.toFixed(1) + "%";
        document.getElementById("disk-progress").style.width = data.disk.usage_percent + "%";

        // Overall status + anomaly panel
        updateOverallStatus(data.overall_status);
        updateAnomalyPanel(data.overall_status);

        document.getElementById("last-updated").textContent =
            "Last updated: " + new Date().toLocaleTimeString();

        console.log("Metrics updated:", data);

    } catch (error) {
        console.error("Error loading metrics:", error);

        document.getElementById("last-updated").textContent =
            "⚠ Unable to connect to server";
    }
}

/* Load metrics immediately */
loadMetrics();

/* Refresh every 3 seconds */
setInterval(loadMetrics, 3000);
