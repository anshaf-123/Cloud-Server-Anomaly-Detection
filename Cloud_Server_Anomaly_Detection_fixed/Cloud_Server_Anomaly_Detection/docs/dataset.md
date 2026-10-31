# Dataset Documentation

This document describes the dataset used in the **Intelligent Cloud Server Anomaly Detection and Real-Time Monitoring System**. To ensure reproducibility and transparency, we utilize real-world server performance telemetry from a recognized public benchmark, and supplement missing metrics using mathematically reasonable derivations.

---

## 1. Dataset Source
We use telemetry data from the **Numenta Anomaly Benchmark (NAB)**, specifically the `realAWSCloudwatch/` subset. This subset contains real-world system performance metrics from Amazon EC2 instances, RDS databases, and Elastic Load Balancers (ELBs).

- **Source Repository**: [numenta/NAB](https://github.com/numenta/NAB)
- **Time Frequency**: 5-minute sampling intervals.
- **Duration**: 14 days of monitoring per server (4,032 observations per server).

---

## 2. Server Mapping & Raw Telemetry Files
We map specific raw files from NAB to create three distinct server profiles:

| Server ID | Metric | Raw NAB File Used | Description | Real/Synthetic |
| :--- | :--- | :--- | :--- | :--- |
| **SERVER-01** | CPU Utilization | `ec2_cpu_utilization_5f5533.csv` | Active CPU usage % of an EC2 instance. | **Real** |
| | Network Traffic | `ec2_network_in_257a54.csv` | Incoming traffic (rescaled to MB/s). | **Real** |
| | Disk Write I/O | `ec2_disk_write_bytes_1ef3de.csv` | Disk write throughput (rescaled to MB/s). | **Real** |
| | Memory Usage | *Derived* | System memory utilization %. | **Derived** |
| | Response Time | *Derived* | Client request response latency in ms. | **Derived** |
| | Request Rate | *Derived* | Average request count per second. | **Derived** |
| **SERVER-02** | CPU Utilization | `ec2_cpu_utilization_ac20cd.csv` | Active CPU usage % of an EC2 instance. | **Real** |
| | Network Traffic | `ec2_network_in_5abac7.csv` | Incoming traffic (rescaled to MB/s). | **Real** |
| | Disk Write I/O | `ec2_disk_write_bytes_c0d644.csv` | Disk write throughput (rescaled to MB/s). | **Real** |
| | Memory Usage | *Derived* | System memory utilization %. | **Derived** |
| | Response Time | *Derived* | Client request response latency in ms. | **Derived** |
| | Request Rate | *Derived* | Average request count per second. | **Derived** |
| **SERVER-03** | CPU Utilization | `rds_cpu_utilization_cc0c53.csv` | CPU usage % of an Amazon RDS instance. | **Real** |
| | Request Rate | `elb_request_count_8c0756.csv` | ELB request count per 5-minute window. | **Real** |
| | Network Traffic | *Derived* | Simulated network traffic based on CPU load. | **Derived** |
| | Disk Write I/O | *Derived* | Simulated disk write throughput based on CPU load. | **Derived** |
| | Memory Usage | *Derived* | System memory utilization %. | **Derived** |
| | Response Time | *Derived* | Client request response latency in ms. | **Derived** |

---

## 3. Preprocessing & Temporal Alignment
Because the raw AWS CloudWatch files in the NAB repository cover different time periods (e.g., CPU in February 2014, Network in April 2014), a direct join by calendar timestamp yields missing values. 

To resolve this, we align the telemetry streams by their **sequence row indices** (truncating to the first 4,032 observations, representing a 14-day window). We then assign a unified calendar timeline:
- **Timeline Start**: `2014-02-14 14:27:00`
- **Timeline End**: `2014-02-28 14:22:00`
- **Sampling Frequency**: 5 minutes

This preserves the cyclical patterns (diurnal/nocturnal fluctuations) of each metric while aligning them into a single, cohesive multivariate observation at each timestamp.

---

## 4. Mathematical Derivations of Supplementary Metrics
To display a rich set of resources in the monitoring dashboard, we mathematically derive Memory and Response Time based on system workloads:

### A. Memory Usage (%)
Memory utilization is modeled as a smoothed function of CPU load to capture allocation latency and a higher baseline:
\[\text{Memory Usage} = 40.0 + \left(\text{CPU}_{\text{smoothed}} \times 0.45\right) + \epsilon\]
- **Where**: $\text{CPU}_{\text{smoothed}}$ is a rolling 3-period (15 min) average of CPU utilization, and $\epsilon \sim \mathcal{N}(0, 1.5)$ is Gaussian white noise. Values are clipped to $[10\%, 98\%]$.

### B. Response Time (ms)
Response time is modeled to reflect system slowdown under high request rates and non-linear exhaustion under high CPU loads:
\[\text{Response Time} = 40.0 + \left(\text{Request Rate} \times 0.15\right) + e^{\frac{\text{CPU}}{20.0}} + \epsilon\]
- **Where**: $\epsilon \sim \mathcal{N}(0, 5)$ is random network latency jitter. Values are clipped to $[5\text{ms}, 2000\text{ms}]$.

---

## 5. Summary Statistics
The combined historical dataset is saved under `data/processed/historical_metrics.csv` and contains:
- **Total Observations**: 12,096 rows
- **Number of Servers**: 3 (SERVER-01, SERVER-02, SERVER-03)
- **Columns**: `timestamp`, `server_id`, `cpu_usage`, `memory_usage`, `disk_usage`, `network_traffic`, `response_time`, `request_rate`
