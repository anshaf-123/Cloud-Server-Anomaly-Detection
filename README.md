# Intelligent Cloud Server Anomaly Detection and Real-Time Monitoring System

This project is a comprehensive, academic-grade anomaly detection and real-time monitoring system designed to monitor cloud server metrics and automatically detect, score, explain, and visualize abnormal behavior in real time.

---

## 1. Problem Statement
Modern cloud infrastructure generates high-volume, high-velocity time-series performance metrics. Manually detecting anomalies (e.g., resource leaks, security intrusions, hardware degradation) across hundreds of servers is impossible. This project implements a modular, scalable, multi-model ensemble detection framework to identify anomalies, calculate confidence and severity, and provide explainable factor contributions.

## 2. Objectives
- **Scaling Big Data**: Build a data processing pipeline using **PySpark** capable of handling large-scale monitoring datasets.
- **Hybrid Detection**: Integrate **statistical analysis (R & Python)** and **Machine Learning models (Scikit-learn)**.
- **Ensemble Voting**: Combine outputs into a weighted ensemble anomaly flag and confidence score.
- **Real-Time Simulation**: Create a realistic multi-server simulator simulating CPU/memory spikes and resource leaks.
- **Explainability**: Quantify feature contributions for each anomaly (e.g., identifying CPU vs. network spikes).
- **Persistent Storage**: Save metrics, predictions, and explanations in a normalized **MySQL** database.
- **Web Dashboard**: Provide a responsive **PHP/JS** interface displaying real-time metrics and alerts.

---

## 3. Technology Stack & Roles
- **Python (3.11.x)**: Core processing, feature engineering, machine learning inference, and simulator orchestration.
- **Jupyter Notebook**: Step-by-step experimentation, exploratory data analysis (EDA), and evaluation.
- **PySpark (3.4+)**: Big Data distributed aggregation and feature calculation.
- **R (4.x)**: Statistical time-series modeling (e.g., IQR and rolling z-score analysis).
- **Scikit-learn**: Machine learning models: Isolation Forest, Local Outlier Factor (LOF), and DBSCAN.
- **MySQL (via XAMPP)**: Relational schema to store server statuses, metric streams, and anomalous events.
- **PHP (8.x)**: Secure REST API backend delivering JSON metrics and anomaly statistics.
- **HTML5 / CSS3 / JavaScript (ES6)**: Real-time web monitoring frontend using **Chart.js**.

---

## 4. Folder Structure
```
Cloud_Server_Anomaly_Detection/
├── data/                    # Dataset storage (raw, processed, synthetic)
├── notebooks/               # Jupyter notebooks for phased analysis (01 to 09)
├── python/                  # Python implementation files (.py)
├── pyspark/                 # Spark preprocessing and aggregation pipelines
├── r/                       # R statistical scripts
├── models/                  # Saved serialized model binaries (.joblib)
├── results/                 # Evaluation figures, reports, and predictions
├── database/                # MySQL schema.sql and seed.sql
├── website/                 # PHP API backend and JS dashboard frontend
├── tests/                   # Automated unit and integration tests
├── docs/                    # Detailed design and model documentation
├── requirements.txt         # Python package dependencies
├── .env.example             # Configuration settings template
└── verify_setup.py          # Environment diagnostics utility
```

---

## 5. System Setup & Installation

### A. Python Environment
1. Open the Anaconda Prompt.
2. Activate your environment:
   ```bash
   conda activate cloud_anomaly
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### B. Java Installation (for PySpark)
1. Download and install **Java JDK 11** or **8** (e.g., AdoptOpenJDK).
2. Set your `JAVA_HOME` environment variable to your Java installation path (e.g., `C:\Program Files\Java\jdk-11`).
3. Add `%JAVA_HOME%\bin` to your system `PATH`.

### C. R Installation (for R Statistical Analysis)
1. Download and install **R for Windows** (v4.x) from [CRAN](https://cran.r-project.org/).
2. Add the R binary path (e.g., `C:\Program Files\R\R-4.x.x\bin\x64`) to your system `PATH` so that `Rscript` is runnable.

### D. MySQL & PHP Backend (XAMPP Setup)
1. Open **XAMPP Control Panel** and start **Apache** and **MySQL**.
2. Create a symbolic link (junction) to make the website files live in XAMPP:
   * Open CMD as Administrator and run:
     ```cmd
     mklink /J "C:\xampp\htdocs\cloud_anomaly" "c:\Users\Muhammed Anzil\Downloads\Cloud_Server_Anomaly_Detection\website"
     ```
3. Open `http://localhost/phpmyadmin` and import the schema from `database/schema.sql` (to be created in Phase 16).

---

## 6. How to Run Setup Verification
Run the diagnostics script to check your local environment settings:
```bash
python verify_setup.py
```
This will print a detailed status report of your Python version, package library installations, Java/R runtimes, and MySQL server connectivity.
