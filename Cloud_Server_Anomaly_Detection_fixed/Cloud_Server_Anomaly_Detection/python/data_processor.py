import pandas as pd
import numpy as np
import joblib
import logging
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Handles preprocessing, scaling, and preparation of server metrics.
    Saves scaler states to disk for consistency during online/real-time inference.
    """
    METRIC_COLUMNS = ["cpu_usage", "memory_usage", "disk_usage", "network_traffic", "response_time", "request_rate"]

    def __init__(self, scaler_path: str = "models/scaler.joblib"):
        self.scaler_path = Path(scaler_path)
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fits the MinMaxScaler on training data and transforms the metrics."""
        logger.info("Fitting and transforming server metrics using MinMaxScaler...")
        df_scaled = df.copy()
        
        # Fit and transform
        scaled_values = self.scaler.fit_transform(df[self.METRIC_COLUMNS])
        
        # Add scaled columns
        for idx, col in enumerate(self.METRIC_COLUMNS):
            df_scaled[f"scaled_{col}"] = scaled_values[:, idx]
            
        # Ensure model directory exists and save the scaler
        self.scaler_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.scaler, self.scaler_path)
        logger.info(f"Saved fitted MinMaxScaler to {self.scaler_path}")
        
        return df_scaled

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforms data using the saved scaler (for real-time inference or testing)."""
        if not self.scaler_path.exists():
            raise FileNotFoundError(f"Fitted scaler not found at {self.scaler_path}. Run fit_transform first.")
            
        logger.debug("Loading scaler for transformation...")
        loaded_scaler = joblib.load(self.scaler_path)
        df_scaled = df.copy()
        
        # Transform
        scaled_values = loaded_scaler.transform(df[self.METRIC_COLUMNS])
        
        # Add scaled columns
        for idx, col in enumerate(self.METRIC_COLUMNS):
            df_scaled[f"scaled_{col}"] = scaled_values[:, idx]
            
        return df_scaled

def run_preprocessing_pipeline(input_csv: str, output_csv: str, scaler_path: str):
    """Loads validated metrics, runs scaling, saves output and scaler."""
    df = pd.read_csv(input_csv)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    processor = DataProcessor(scaler_path)
    df_preprocessed = processor.fit_transform(df)
    
    # Save output
    df_preprocessed.to_csv(output_csv, index=False)
    logger.info(f"Preprocessed dataset (raw + scaled columns) saved to {output_csv}")
    return df_preprocessed

if __name__ == "__main__":
    input_file = "data/processed/validated_historical_metrics.csv"
    output_file = "data/processed/preprocessed_historical_metrics.csv"
    scaler_file = "models/scaler.joblib"
    
    if Path(input_file).exists():
        run_preprocessing_pipeline(input_file, output_file, scaler_file)
    else:
        logger.error(f"Validated metrics file {input_file} not found. Run validation pipeline first.")
