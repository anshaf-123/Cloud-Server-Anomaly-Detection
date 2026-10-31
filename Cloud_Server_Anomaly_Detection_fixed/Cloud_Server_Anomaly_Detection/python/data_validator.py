import os
import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Dict, Any, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class DataValidator:
    """
    Handles validation, cleaning, and quality reporting for server metrics data.
    Designed to support CSV files and easily extensible to JSON/API inputs.
    """
    REQUIRED_COLUMNS = {
        "timestamp": "datetime64[ns]",
        "server_id": "object",
        "cpu_usage": "float64",
        "memory_usage": "float64",
        "disk_usage": "float64",
        "network_traffic": "float64",
        "response_time": "float64",
        "request_rate": "float64"
    }

    def __init__(self, data_path: str = None):
        self.data_path = data_path
        self.df = None
        self.quality_report = {}

    def load_csv(self, path: str = None) -> pd.DataFrame:
        """Loads dataset from CSV file."""
        target_path = path or self.data_path
        if not target_path:
            raise ValueError("No data path specified for loading.")
        
        logger.info(f"Loading data from {target_path}...")
        try:
            self.df = pd.read_csv(target_path)
            logger.info(f"Successfully loaded dataset with {len(self.df)} rows and {len(self.df.columns)} columns.")
            return self.df
        except Exception as e:
            logger.error(f"Failed to load CSV file: {str(e)}")
            raise e

    def load_from_dict(self, records: list) -> pd.DataFrame:
        """Loads dataset from a list of dictionaries (for API/JSON streaming support)."""
        logger.info(f"Ingesting {len(records)} records from dictionary source...")
        self.df = pd.DataFrame(records)
        return self.df

    def validate_schema(self) -> Tuple[bool, list]:
        """Validates that all required columns are present."""
        if self.df is None:
            raise ValueError("No dataset loaded to validate schema.")
        
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in self.df.columns]
        is_valid = len(missing_cols) == 0
        
        self.quality_report["schema_valid"] = is_valid
        self.quality_report["missing_columns"] = missing_cols
        
        if not is_valid:
            logger.warning(f"Schema validation failed! Missing columns: {missing_cols}")
        else:
            logger.info("Schema validation passed: all required columns present.")
        
        return is_valid, missing_cols

    def validate_and_cast_types(self) -> Tuple[bool, Dict[str, str]]:
        """Validates column data types and casts them to the appropriate format."""
        if self.df is None:
            raise ValueError("No dataset loaded to validate data types.")
        
        type_errors = {}
        
        # Parse timestamp column first
        if "timestamp" in self.df.columns:
            try:
                self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
                logger.info("Successfully cast 'timestamp' column to datetime.")
            except Exception as e:
                type_errors["timestamp"] = f"Failed to cast to datetime: {str(e)}"
                logger.error(f"Timestamp conversion failed: {str(e)}")

        # Check and cast numerical columns
        for col, expected_type in self.REQUIRED_COLUMNS.items():
            if col == "timestamp" or col not in self.df.columns:
                continue
            
            try:
                if expected_type == "float64":
                    self.df[col] = pd.to_numeric(self.df[col], errors="raise").astype(float)
                elif expected_type == "object":
                    self.df[col] = self.df[col].astype(str)
            except Exception as e:
                type_errors[col] = f"Expected {expected_type}, failed to cast: {str(e)}"
                logger.error(f"Data type conversion failed for column '{col}': {str(e)}")

        is_valid = len(type_errors) == 0
        self.quality_report["types_valid"] = is_valid
        self.quality_report["type_errors"] = type_errors
        
        return is_valid, type_errors

    def check_quality(self) -> Dict[str, Any]:
        """Performs missing value checks, duplicate checks, and range bounds checking."""
        if self.df is None:
            raise ValueError("No dataset loaded to perform quality checks.")
        
        total_rows = len(self.df)
        
        # 1. Missing Values
        missing_counts = self.df.isnull().sum().to_dict()
        missing_percentages = {col: (count / total_rows) * 100 for col, count in missing_counts.items()}
        
        # 2. Duplicate Records (based on timestamp + server_id)
        duplicate_count = 0
        if "timestamp" in self.df.columns and "server_id" in self.df.columns:
            duplicate_count = self.df.duplicated(subset=["timestamp", "server_id"]).sum()
            
        # 3. Invalid Value Ranges (outliers / illogical measurements)
        range_violations = {}
        
        # CPU usage bounds [0, 100]
        if "cpu_usage" in self.df.columns:
            cpu_viols = ((self.df["cpu_usage"] < 0) | (self.df["cpu_usage"] > 100)).sum()
            range_violations["cpu_usage_violations"] = int(cpu_viols)
            
        # Memory usage bounds [0, 100]
        if "memory_usage" in self.df.columns:
            mem_viols = ((self.df["memory_usage"] < 0) | (self.df["memory_usage"] > 100)).sum()
            range_violations["memory_usage_violations"] = int(mem_viols)
            
        # Disk usage (throughput or percentage) must be >= 0
        if "disk_usage" in self.df.columns:
            disk_viols = (self.df["disk_usage"] < 0).sum()
            range_violations["disk_usage_violations"] = int(disk_viols)
            
        # Network traffic must be >= 0
        if "network_traffic" in self.df.columns:
            net_viols = (self.df["network_traffic"] < 0).sum()
            range_violations["network_traffic_violations"] = int(net_viols)
            
        # Response time must be >= 0
        if "response_time" in self.df.columns:
            rt_viols = (self.df["response_time"] < 0).sum()
            range_violations["response_time_violations"] = int(rt_viols)
            
        # Request rate must be >= 0
        if "request_rate" in self.df.columns:
            rr_viols = (self.df["request_rate"] < 0).sum()
            range_violations["request_rate_violations"] = int(rr_viols)

        # 4. Compilation of Quality Metrics
        self.quality_report.update({
            "total_rows": total_rows,
            "missing_counts": missing_counts,
            "missing_percentages": missing_percentages,
            "duplicate_records": int(duplicate_count),
            "range_violations": range_violations
        })
        
        logger.info(f"Quality Check Completed. Missing values: {sum(missing_counts.values())}, Duplicates: {duplicate_count}, Range violations: {sum(range_violations.values())}")
        return self.quality_report

    def clean_data(self) -> pd.DataFrame:
        """Cleans the dataset by removing duplicate keys and sorting chronologically."""
        if self.df is None:
            raise ValueError("No dataset loaded to clean.")
        
        # Remove duplicates
        initial_count = len(self.df)
        if "timestamp" in self.df.columns and "server_id" in self.df.columns:
            self.df = self.df.drop_duplicates(subset=["timestamp", "server_id"], keep="first")
            removed = initial_count - len(self.df)
            if removed > 0:
                logger.info(f"Removed {removed} duplicate server metric records.")
        
        # Sort chronologically by server
        self.df = self.df.sort_values(by=["server_id", "timestamp"]).reset_index(drop=True)
        logger.info("Dataset sorted chronologically by server_id and timestamp.")
        
        return self.df

    def print_quality_report(self):
        """Prints a well-formatted Data Quality Report to console."""
        print("\n" + "="*50)
        print("           DATA QUALITY REPORT")
        print("="*50)
        print(f"Total Observations : {self.quality_report.get('total_rows', 0)}")
        print(f"Schema Validation  : {'PASSED' if self.quality_report.get('schema_valid') else 'FAILED'}")
        print(f"Type Validation    : {'PASSED' if self.quality_report.get('types_valid') else 'FAILED'}")
        print(f"Duplicate Records  : {self.quality_report.get('duplicate_records', 0)}")
        
        print("\nMissing Values:")
        for col, count in self.quality_report.get("missing_counts", {}).items():
            pct = self.quality_report["missing_percentages"][col]
            print(f"  - {col:<18} : {count} ({pct:.2f}%)")
            
        print("\nRange Violations (Negative/Out-of-Bounds):")
        for metric, viols in self.quality_report.get("range_violations", {}).items():
            print(f"  - {metric:<25} : {viols}")
        print("="*50 + "\n")

def run_validation_pipeline(input_csv: str, output_csv: str) -> pd.DataFrame:
    """Ingests a CSV, runs the validation pipeline, prints report, and saves cleaned data."""
    validator = DataValidator(input_csv)
    validator.load_csv()
    
    # Run validations
    validator.validate_schema()
    validator.validate_and_cast_types()
    validator.check_quality()
    validator.print_quality_report()
    
    # Clean data
    cleaned_df = validator.clean_data()
    
    # Save cleaned data
    cleaned_df.to_csv(output_csv, index=False)
    logger.info(f"Saved cleaned and validated dataset to {output_csv}")
    return cleaned_df

if __name__ == "__main__":
    import sys
    # Paths relative to workspace root
    input_file = "data/processed/historical_metrics.csv"
    output_file = "data/processed/validated_historical_metrics.csv"
    
    if os.path.exists(input_file):
        run_validation_pipeline(input_file, output_file)
    else:
        logger.error(f"Input file {input_file} does not exist. Run python/data_loader.py first.")
