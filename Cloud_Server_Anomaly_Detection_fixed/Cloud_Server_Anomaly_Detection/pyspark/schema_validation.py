from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .appName("CloudAnomalySchemaValidation")
    .master("local[*]")
    .getOrCreate()
)

input_file = "data/processed/features_historical_metrics.csv"

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_file)
)

print("\n===== CLOUD ANOMALY DATASET SCHEMA =====")
df.printSchema()

print("\n===== DATASET INFORMATION =====")
print("Rows:", df.count())
print("Columns:", len(df.columns))

print("\n===== COLUMN NAMES =====")
print(df.columns)

print("\n===== SAMPLE RECORDS =====")
df.show(5, truncate=False)

spark.stop()