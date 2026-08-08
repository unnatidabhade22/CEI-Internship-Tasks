import os
import csv
from datetime import datetime

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data"
)

CUSTOMERS_FILE = os.path.join(
    DATA_DIR,
    "silver",
    "customers",
    "customers_silver_validated.csv"
)

ORDERS_FILE = os.path.join(
    DATA_DIR,
    "silver",
    "orders",
    "orders_silver_final.csv"
)

GOLD_DIR = os.path.join(
    DATA_DIR,
    "gold"
)

OUTPUT_FILE = os.path.join(
    GOLD_DIR,
    "customer_ltv.csv"
)

os.makedirs(
    GOLD_DIR,
    exist_ok=True
)

# ============================================================
# SPARK TEMP
# ============================================================

SPARK_TEMP = r"D:\spark-temp"

os.makedirs(
    SPARK_TEMP,
    exist_ok=True
)

os.environ["TEMP"] = SPARK_TEMP
os.environ["TMP"] = SPARK_TEMP
os.environ["SPARK_LOCAL_DIRS"] = SPARK_TEMP

# ============================================================
# START SPARK
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("GoldCustomerLTV")
    .master("local[2]")
    .config("spark.local.dir", SPARK_TEMP)
    .config("spark.sql.shuffle.partitions", "2")
    .config("spark.default.parallelism", "2")
    .config("spark.hadoop.fs.permissions.enabled", "false")
    .config("spark.hadoop.io.native.lib.available", "false")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("=" * 70)
print("CREATING GOLD - CUSTOMER LTV")
print("=" * 70)

# ============================================================
# LOAD CUSTOMERS
# ============================================================

print("\nLoading Silver customers...")

customers = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(CUSTOMERS_FILE)
)

print(f"Customers loaded: {customers.count()}")

# ============================================================
# LOAD ORDERS
# ============================================================

print("\nLoading Silver orders...")

orders = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(ORDERS_FILE)
)

print(f"Orders loaded: {orders.count()}")

# ============================================================
# PREPARE ORDERS
# ============================================================

orders = (
    orders
    .withColumn(
        "order_date",
        F.to_timestamp("order_date")
    )
    .withColumn(
        "total_amount",
        F.col("total_amount").cast("double")
    )
    .withColumn(
        "status",
        F.lower(
            F.trim(
                F.col("status")
            )
        )
    )
)

# ============================================================
# EXCLUDE CANCELLED ORDERS
# ============================================================

orders = orders.filter(
    F.col("status") != "cancelled"
)

# ============================================================
# FIND MAX ORDER DATE
# ============================================================

max_order_date = (
    orders
    .agg(
        F.max("order_date").alias("max_date")
    )
    .collect()[0]["max_date"]
)

print(
    f"\nLatest order date: {max_order_date}"
)

# ============================================================
# CUSTOMER METRICS
# ============================================================

print("\nCalculating customer metrics...")

customer_metrics = (
    orders
    .groupBy("customer_id")
    .agg(
        F.round(
            F.sum("total_amount"),
            2
        ).alias("lifetime_spend"),

        F.countDistinct(
            "order_id"
        ).alias("order_frequency"),

        F.max(
            "order_date"
        ).alias("last_order_date")
    )
)

# ============================================================
# RECENCY
# ============================================================

customer_metrics = customer_metrics.withColumn(
    "recency_days",
    F.datediff(
        F.lit(max_order_date),
        F.col("last_order_date")
    )
)

# ============================================================
# JOIN WITH CUSTOMERS
# ============================================================

ltv = (
    customers
    .select(
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "city",
        "state",
        "region"
    )
    .join(
        customer_metrics,
        on="customer_id",
        how="left"
    )
)

# ============================================================
# FILL CUSTOMERS WITH NO ORDERS
# ============================================================

ltv = (
    ltv
    .fillna(
        {
            "lifetime_spend": 0.0,
            "order_frequency": 0,
            "recency_days": -1
        }
    )
)

# ============================================================
# CUSTOMER SEGMENT
#
# VIP       >= 100,000
# High Value >= 50,000
# Mid Value  >= 20,000
# Low Value  < 20,000
# ============================================================

ltv = ltv.withColumn(
    "customer_segment",
    F.when(
        F.col("lifetime_spend") >= 100000,
        "VIP"
    )
    .when(
        F.col("lifetime_spend") >= 50000,
        "High Value"
    )
    .when(
        F.col("lifetime_spend") >= 20000,
        "Mid Value"
    )
    .otherwise(
        "Low Value"
    )
)

# ============================================================
# FINAL COLUMNS
# ============================================================

ltv = ltv.select(
    "customer_id",
    "first_name",
    "last_name",
    "email",
    "city",
    "state",
    "region",
    "lifetime_spend",
    "order_frequency",
    "last_order_date",
    "recency_days",
    "customer_segment"
)

# ============================================================
# COLLECT
# ============================================================

print("\nPreparing Customer LTV result...")

result = (
    ltv
    .orderBy("customer_id")
    .collect()
)

# ============================================================
# WRITE CSV USING PYTHON
# ============================================================

print("Writing Gold CSV...")

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "city",
        "state",
        "region",
        "lifetime_spend",
        "order_frequency",
        "last_order_date",
        "recency_days",
        "customer_segment"
    ])

    for row in result:

        writer.writerow([
            row["customer_id"],
            row["first_name"],
            row["last_name"],
            row["email"],
            row["city"],
            row["state"],
            row["region"],
            row["lifetime_spend"],
            row["order_frequency"],
            row["last_order_date"],
            row["recency_days"],
            row["customer_segment"]
        ])

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("CUSTOMER LTV CREATED SUCCESSFULLY")
print("=" * 70)

print(
    f"Output file: {OUTPUT_FILE}"
)

print(
    f"Gold rows: {len(result):,}"
)

# ============================================================
# KPI SUMMARY
# ============================================================

total_customers = len(result)

active_customers = (
    ltv
    .filter(
        F.col("order_frequency") > 0
    )
    .count()
)

average_ltv = (
    ltv
    .agg(
        F.avg("lifetime_spend").alias("avg_ltv")
    )
    .collect()[0]["avg_ltv"]
)

print("\nCustomer LTV Summary")
print("-" * 50)

print(
    f"Total customers: "
    f"{total_customers:,}"
)

print(
    f"Active customers: "
    f"{active_customers:,}"
)

print(
    f"Active customer rate: "
    f"{active_customers / total_customers * 100:.2f}%"
)

print(
    f"Average LTV: "
    f"{average_ltv:,.2f}"
)

# ============================================================
# SEGMENT SUMMARY
# ============================================================

print("\nCustomer Segment Summary")
print("-" * 50)

segment_counts = (
    ltv
    .groupBy("customer_segment")
    .count()
    .orderBy("customer_segment")
    .collect()
)

for row in segment_counts:

    print(
        f"{row['customer_segment']}: "
        f"{row['count']:,}"
    )

# ============================================================
# SAMPLE
# ============================================================

print("\nSample:")

for row in result[:10]:

    print(
        row["customer_id"],
        "|",
        row["first_name"],
        row["last_name"],
        "| Spend:",
        row["lifetime_spend"],
        "| Orders:",
        row["order_frequency"],
        "| Recency:",
        row["recency_days"],
        "days",
        "| Segment:",
        row["customer_segment"]
    )

print("\nStatus: SUCCESS")

spark.stop()

print("\nSpark stopped successfully.")