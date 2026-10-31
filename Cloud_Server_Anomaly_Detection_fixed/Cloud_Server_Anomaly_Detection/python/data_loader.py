import os
import urllib.request
import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Base URLs for official Numenta Anomaly Benchmark data
NAB_RAW_URL = "https://raw.githubusercontent.com/numenta/NAB/master/data/realAWSCloudwatch/"

# Raw dataset files to download
DATA_FILES = {
    # Server 1 files
    "server_1_cpu.csv": "ec2_cpu_utilization_5f5533.csv",
    "server_1_network.csv": "ec2_network_in_257a54.csv",
    "server_1_disk.csv": "ec2_disk_write_bytes_1ef3de.csv",
    
    # Server 2 files
    "server_2_cpu.csv": "ec2_cpu_utilization_ac20cd.csv",
    "server_2_network.csv": "ec2_network_in_5abac7.csv",
    "server_2_disk.csv": "ec2_disk_write_bytes_c0d644.csv",
    
    # Server 3 files
    "server_3_cpu.csv": "rds_cpu_utilization_cc0c53.csv",
    "server_3_requests.csv": "elb_request_count_8c0756.csv"
}

def download_raw_data(dest_dir: Path):
    """Downloads raw AWS CloudWatch metrics from Numenta Anomaly Benchmark."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Downloading raw datasets to {dest_dir}...")
    
    for local_name, remote_name in DATA_FILES.items():
        url = f"{NAB_RAW_URL}{remote_name}"
        local_path = dest_dir / local_name
        
        if local_path.exists():
            logger.info(f"  [+] {local_name} already exists. Skipping download.")
            continue
            
        try:
            logger.info(f"  [-] Downloading {url} -> {local_name}...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read()
                with open(local_path, "wb") as f:
                    f.write(content)
            logger.info(f"  [+] Saved {local_name}")
        except Exception as e:
            logger.error(f"  [x] Failed to download {local_name}: {str(e)}")
            raise e

def load_and_align_datasets(raw_dir: Path, processed_dir: Path):
    """Loads raw data, aligns sequence indices, derives missing metrics, and saves processed data."""
    processed_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Aligning and merging datasets by sequence index...")
    
    # Target length is 4032 (exactly 14 days of 5-minute interval metrics)
    target_length = 4032
    
    # Generate unified datetime index for the 14-day window
    base_timestamps = pd.date_range(start="2014-02-14 14:27:00", periods=target_length, freq="5min")
    
    servers = {
        "SERVER-01": {
            "cpu_file": "server_1_cpu.csv",
            "network_file": "server_1_network.csv",
            "disk_file": "server_1_disk.csv",
            "has_requests": False
        },
        "SERVER-02": {
            "cpu_file": "server_2_cpu.csv",
            "network_file": "server_2_network.csv",
            "disk_file": "server_2_disk.csv",
            "has_requests": False
        },
        "SERVER-03": {
            "cpu_file": "server_3_cpu.csv",
            "network_file": None,
            "disk_file": None,
            "requests_file": "server_3_requests.csv",
            "has_requests": True
        }
    }
    
    combined_records = []
    
    for server_id, sources in servers.items():
        logger.info(f"Processing metrics for {server_id}...")
        
        # Load CPU
        cpu_path = raw_dir / sources["cpu_file"]
        df_cpu = pd.read_csv(cpu_path).iloc[:target_length]
        cpu_vals = df_cpu["value"].clip(0, 100).values
        
        # Adjust CPU scale if too low/high
        # NAB CPU values are sometimes very low, let's normalize or scale them slightly for realistic server load (e.g. 5% to 95%)
        # server 1: EC2 instance, CPU is already in a good scale. Server 3: RDS, scale is good.
        
        # Load or simulate Network In
        if sources["network_file"]:
            net_path = raw_dir / sources["network_file"]
            df_net = pd.read_csv(net_path).iloc[:target_length]
            # Convert bytes to MB
            net_vals = (df_net["value"].values / (1024 * 1024)).clip(0.1, 1000)
        else:
            # Simulate network traffic correlated with CPU usage
            net_vals = (cpu_vals * 0.15 + np.random.normal(5, 1, target_length)).clip(1, 100)
            
        # Load or simulate Disk usage
        if sources["disk_file"]:
            disk_path = raw_dir / sources["disk_file"]
            df_disk = pd.read_csv(disk_path).iloc[:target_length]
            # Convert bytes to MB
            disk_vals = (df_disk["value"].values / (1024 * 1024)).clip(0.1, 500)
        else:
            # Simulate disk usage (%)
            disk_vals = (25 + cpu_vals * 0.1 + np.random.normal(0, 2, target_length)).clip(5, 95)
            
        # Load or simulate Request rate
        if sources.get("requests_file"):
            req_path = raw_dir / sources["requests_file"]
            df_req = pd.read_csv(req_path).iloc[:target_length]
            req_vals = df_req["value"].values
        else:
            # Simulate request rate (requests/sec) based on CPU usage
            req_vals = (cpu_vals * 1.5 + np.random.normal(15, 3, target_length)).clip(1, 300)
            
        # ------------------------------------------------------------
        # MATHEMATICAL DERIVATION OF MISSING FIELDS (Memory & Response Time)
        # ------------------------------------------------------------
        # 1. Memory Usage (%): Baseline = 40%, increases up to 90% as CPU increases
        # We smooth CPU usage using a rolling average to simulate memory allocation delay
        cpu_series = pd.Series(cpu_vals)
        cpu_smoothed = cpu_series.rolling(window=3, min_periods=1).mean().values
        mem_vals = (40.0 + cpu_smoothed * 0.45 + np.random.normal(0, 1.5, target_length)).clip(10, 98)
        
        # 2. Response Time (ms): Increases exponentially with CPU load and request rate
        rt_vals = (
            40.0 
            + req_vals * 0.15 
            + np.exp(cpu_vals / 20.0) 
            + np.random.normal(0, 5, target_length)
        ).clip(5, 2000)
        
        # Build dataframe with unified timestamps
        df_server = pd.DataFrame({
            "timestamp": base_timestamps,
            "server_id": server_id,
            "cpu_usage": cpu_vals,
            "memory_usage": mem_vals,
            "disk_usage": disk_vals,
            "network_traffic": net_vals,
            "response_time": rt_vals,
            "request_rate": req_vals
        })
        
        combined_records.append(df_server)
        
    # Concatenate all servers
    df_all = pd.concat(combined_records, ignore_index=True)
    
    # Sort chronologically by timestamp and server_id
    df_all = df_all.sort_values(by=["timestamp", "server_id"]).reset_index(drop=True)
    
    # Save to processed directory
    output_path = processed_dir / "historical_metrics.csv"
    df_all.to_csv(output_path, index=False)
    logger.info(f"Successfully created merged dataset with {len(df_all)} observations.")
    logger.info(f"Processed dataset saved to {output_path}")

if __name__ == "__main__":
    raw = Path("data/raw")
    processed = Path("data/processed")
    download_raw_data(raw)
    load_and_align_datasets(raw, processed)
