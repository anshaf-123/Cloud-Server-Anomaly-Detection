from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp

spark = (
    SparkSession.builder
    .appName("CloudAnomalyDataLoading")
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

print("\n===== ORIGINAL DATA =====")
print("Rows:", df.count())
print("Columns:", len(df.columns))

if "timestamp" in df.columns:
    df = df.withColumn(
        "timestamp",
        to_timestamp(col("timestamp"))
    )

df = df.dropna(how="all")

print("\n===== AFTER TRANSFORMATION =====")
print("Rows:", df.count())
print("Columns:", len(df.columns))

print("\n===== SAMPLE DATA =====")
df.show(5, truncate=False)

output_path = "data/processed/pyspark_loaded"

df.write.mode("overwrite").option("header", "true").csv(output_path)

print("\n===== OUTPUT =====")
print("Saved to:", output_path)

spark.stop()