
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_unixtime,
    to_timestamp
)
from awsglue.context import GlueContext


# Create Spark session
spark = SparkSession.builder.appName(
    "CryptoBronzeToSilver"
).getOrCreate()

# Create Glue context
glue_context = GlueContext(spark.sparkContext)


# Read Bronze data through Glue Data Catalog
bronze_dyf = glue_context.create_dynamic_frame.from_catalog(
    database="crypto_realtime_db",
    table_name="crypto_trades"
)

# Convert DynamicFrame to Spark DataFrame
df = bronze_dyf.toDF()


# Convert millisecond timestamps to proper timestamps
df = df.withColumn(
    "trade_time",
    to_timestamp(
        from_unixtime(col("trade_time_ms") / 1000)
    )
)

df = df.withColumn(
    "ingested_at",
    to_timestamp(
        from_unixtime(col("ingested_at_ms") / 1000)
    )
)


# Normalize trade_id
# Bronze trade_id is stored as a struct with int and long fields.
# The long field contains the actual trade ID.
df = df.withColumn(
    "trade_id",
    col("trade_id.long").cast("long")
)


# Normalize numeric columns
df = df.withColumn(
    "price",
    col("price").cast("double")
)

df = df.withColumn(
    "quantity",
    col("quantity").cast("double")
)


# Calculate total value of each trade
df = df.withColumn(
    "trade_value",
    col("price") * col("quantity")
)


# Select clean Silver columns
silver_df = df.select(
    "symbol",
    "trade_id",
    "price",
    "quantity",
    "trade_value",
    "is_buyer_maker",
    "trade_time",
    "ingested_at"
)


# Remove duplicate trades
silver_df = silver_df.dropDuplicates(
    ["symbol", "trade_id"]
)


# Write Silver data as Parquet
# Overwrite is intentional for this repair run because
# the previous Silver files had an incorrect trade_id schema.
silver_df.write \
    .mode("overwrite") \
    .partitionBy("symbol") \
    .parquet(
        "s3://maham-crypto-pipeline-2026-246312965173/"
        "silver/trades/"
    )


# Stop Spark
spark.stop()

