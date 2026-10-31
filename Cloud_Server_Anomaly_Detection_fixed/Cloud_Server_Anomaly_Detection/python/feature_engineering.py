import pandas as pd
import numpy as np
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class FeatureEngineer:
    """
    Constructs statistical, rolling, and temporal features from server metrics.
    Ensures calculations are grouped by server_id to avoid cross-server data leakage.
    Uses only look-back windows to prevent future-lookahead data leakage.
    """
    def __init__(self, window_size: int = 12):
        # 12 steps represent a 1-hour window (at 5-minute sampling intervals)
        self.window_size = window_size

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Computes all engineered features on the input dataframe."""
        logger.info("Starting feature engineering calculations...")
        df_feat = df.copy()
        df_feat["timestamp"] = pd.to_datetime(df_feat["timestamp"])
        df_feat = df_feat.sort_values(by=["server_id", "timestamp"]).reset_index(drop=True)

        # 1. Time since previous record (in seconds)
        logger.info("Calculating temporal delta features...")
        df_feat["time_since_previous_record"] = df_feat.groupby("server_id")["timestamp"].diff().dt.total_seconds().fillna(300.0)

        # 2. First-Order Difference (Changes / Workload Shifts)
        logger.info("Calculating first-order differences (metric changes)...")
        for col in ["cpu_usage", "memory_usage", "network_traffic", "response_time"]:
            df_feat[f"{col}_change"] = df_feat.groupby("server_id")[col].diff().fillna(0.0)

        # 3. Rolling Moving Averages (1-hour baseline)
        logger.info(f"Calculating rolling moving averages (window={self.window_size} steps)...")
        for col in ["cpu_usage", "memory_usage", "network_traffic", "response_time"]:
            df_feat[f"{col}_moving_average"] = (
                df_feat.groupby("server_id")[col]
                .rolling(window=self.window_size, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
            )

        # 4. Rolling Standard Deviations (Volatility)
        logger.info(f"Calculating rolling standard deviations (window={self.window_size} steps)...")
        for col in ["cpu_usage", "memory_usage", "network_traffic"]:
            df_feat[f"{col}_rolling_std"] = (
                df_feat.groupby("server_id")[col]
                .rolling(window=self.window_size, min_periods=1)
                .std()
                .reset_index(level=0, drop=True)
                .fillna(0.0)
            )

        # 5. Rolling Min and Max (Limits)
        logger.info(f"Calculating rolling min and max values (window={self.window_size} steps)...")
        df_feat["cpu_rolling_min"] = (
            df_feat.groupby("server_id")["cpu_usage"]
            .rolling(window=self.window_size, min_periods=1)
            .min()
            .reset_index(level=0, drop=True)
        )
        df_feat["cpu_rolling_max"] = (
            df_feat.groupby("server_id")["cpu_usage"]
            .rolling(window=self.window_size, min_periods=1)
            .max()
            .reset_index(level=0, drop=True)
        )

        # 6. Deviation from Moving Average
        logger.info("Calculating deviations from moving averages...")
        for col in ["cpu_usage", "memory_usage", "network_traffic", "response_time"]:
            df_feat[f"{col}_dev_from_ma"] = df_feat[col] - df_feat[f"{col}_moving_average"]

        logger.info(f"Calculated {len(df_feat.columns) - len(df.columns)} new features.")
        return df_feat

def run_feature_engineering_pipeline(input_csv: str, output_csv: str, window_size: int = 12):
    """Loads preprocessed data, runs feature engineering, and saves result."""
    df = pd.read_csv(input_csv)
    
    engineer = FeatureEngineer(window_size)
    df_features = engineer.fit_transform(df)
    
    df_features.to_csv(output_csv, index=False)
    logger.info(f"Features dataset saved successfully to {output_csv}")
    return df_features

if __name__ == "__main__":
    input_file = "data/processed/preprocessed_historical_metrics.csv"
    output_file = "data/processed/features_historical_metrics.csv"
    
    if Path(input_file).exists():
        run_feature_engineering_pipeline(input_file, output_file)
    else:
        logger.error(f"Preprocessed file {input_file} not found. Run preprocessing pipeline first.")
