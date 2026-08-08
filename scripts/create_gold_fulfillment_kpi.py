import os
import csv

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
    "fulfillment_kpi.csv"
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
    .appName("GoldFulfillmentKPI")
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
print("CREATING GOLD - FULFILLMENT KPI")
print("=" * 70)

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
# PREPARE DATA
# ============================================================

orders = orders.withColumn(
    "order_date",
    F.to_timestamp("order_date")
)

orders = orders.withColumn(
    "date",
    F.to_date("order_date")
)

orders = orders.withColumn(
    "status",
    F.lower(
        F.trim(
            F.col("status")
        )
    )
)

# ============================================================
# FULFILLMENT KPI
# ============================================================

kpi = (
    orders
    .groupBy(
        "date",
        "warehouse_id",
        "region"
    )
    .agg(
        F.countDistinct(
            "order_id"
        ).alias("total_orders"),

        F.countDistinct(
            F.when(
                F.col("status") == "delivered",
                F.col("order_id")
            )
        ).alias("delivered_orders"),

        F.countDistinct(
            F.when(
                F.col("status") == "cancelled",
                F.col("order_id")
            )
        ).alias("cancelled_orders"),

        F.countDistinct(
            F.when(
                F.col("status") == "shipped",
                F.col("order_id")
            )
        ).alias("shipped_orders")
    )
)

# ============================================================
# KPI PERCENTAGES
# ============================================================

kpi = (
    kpi
    .withColumn(
        "delivery_rate_pct",
        F.round(
            F.col("delivered_orders")
            / F.col("total_orders")
            * 100,
            2
        )
    )
    .withColumn(
        "cancellation_rate_pct",
        F.round(
            F.col("cancelled_orders")
            / F.col("total_orders")
            * 100,
            2
        )
    )
    .withColumn(
        "shipment_rate_pct",
        F.round(
            F.col("shipped_orders")
            / F.col("total_orders")
            * 100,
            2
        )
    )
)

# ============================================================
# COLLECT RESULT
# ============================================================

print("\nPreparing KPI result...")

result = (
    kpi
    .orderBy(
        "date",
        "warehouse_id",
        "region"
    )
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
        "date",
        "warehouse_id",
        "region",
        "total_orders",
        "delivered_orders",
        "cancelled_orders",
        "shipped_orders",
        "delivery_rate_pct",
        "cancellation_rate_pct",
        "shipment_rate_pct"
    ])

    for row in result:

        writer.writerow([
            row["date"],
            row["warehouse_id"],
            row["region"],
            row["total_orders"],
            row["delivered_orders"],
            row["cancelled_orders"],
            row["shipped_orders"],
            row["delivery_rate_pct"],
            row["cancellation_rate_pct"],
            row["shipment_rate_pct"]
        ])

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FULFILLMENT KPI CREATED SUCCESSFULLY")
print("=" * 70)

print(f"Output file: {OUTPUT_FILE}")
print(f"Gold rows: {len(result)}")

# ============================================================
# OVERALL KPI SUMMARY
# ============================================================

total_orders = orders.count()

delivered = (
    orders
    .filter(F.col("status") == "delivered")
    .count()
)

cancelled = (
    orders
    .filter(F.col("status") == "cancelled")
    .count()
)

shipped = (
    orders
    .filter(F.col("status") == "shipped")
    .count()
)

print("\nOverall KPI Summary")
print("-" * 50)

print(f"Total orders: {total_orders:,}")
print(
    f"Delivery rate: "
    f"{delivered / total_orders * 100:.2f}%"
)
print(
    f"Cancellation rate: "
    f"{cancelled / total_orders * 100:.2f}%"
)
print(
    f"Shipment rate: "
    f"{shipped / total_orders * 100:.2f}%"
)

print("\nSample:")

for row in result[:10]:

    print(
        row["date"],
        "| Warehouse:",
        row["warehouse_id"],
        "| Region:",
        row["region"],
        "| Orders:",
        row["total_orders"],
        "| Delivery:",
        row["delivery_rate_pct"],
        "%",
        "| Cancellation:",
        row["cancellation_rate_pct"],
        "%",
        "| Shipment:",
        row["shipment_rate_pct"],
        "%"
    )

print("\nStatus: SUCCESS")

spark.stop()

print("\nSpark stopped successfully.")