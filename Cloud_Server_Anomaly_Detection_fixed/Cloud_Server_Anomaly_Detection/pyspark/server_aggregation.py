from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max, min, stddev

spark = (
    SparkSession.builder
    .appName("CloudAnomalyServerAggregation")
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

print("\n===== SERVER-WISE AGGREGATION =====")

result = (
    df.groupBy("server_id")
    .agg(
        avg("cpu_usage").alias("avg_cpu_usage"),
        max("cpu_usage").alias("max_cpu_usage"),
        min("cpu_usage").alias("min_cpu_usage"),
        stddev("cpu_usage").alias("std_cpu_usage"),
        avg("memory_usage").alias("avg_memory_usage"),
        avg("network_traffic").alias("avg_network_traffic"),
        avg("response_time").alias("avg_response_time")
    )
)

result.show(truncate=False)

output_path = "data/processed/server_aggregates"

result.write.mode("overwrite").option("header", "true").csv(output_path)

print("\n===== OUTPUT =====")
print("Server aggregation saved to:", output_path)

spark.stop()