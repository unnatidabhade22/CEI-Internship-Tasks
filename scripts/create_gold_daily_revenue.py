import os
import sys
import glob
import shutil

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")

ORDERS_FILE = os.path.join(
    DATA_DIR,
    "silver",
    "orders",
    "orders_silver_final.csv"
)

ORDER_ITEMS_FILE = os.path.join(
    DATA_DIR,
    "silver",
    "order_items",
    "order_items_silver_final.csv"
)

GOLD_DIR = os.path.join(
    DATA_DIR,
    "gold"
)

OUTPUT_FILE = os.path.join(
    GOLD_DIR,
    "daily_revenue.csv"
)

os.makedirs(GOLD_DIR, exist_ok=True)

# ============================================================
# WINDOWS HADOOP CONFIGURATION
# ============================================================

os.environ["HADOOP_HOME"] = PROJECT_ROOT
os.environ["hadoop.home.dir"] = PROJECT_ROOT

os.environ["PATH"] = (
    os.path.join(PROJECT_ROOT, "bin")
    + os.pathsep
    + os.environ.get("PATH", "")
)

PYTHON_EXECUTABLE = sys.executable

os.environ["PYSPARK_PYTHON"] = PYTHON_EXECUTABLE
os.environ["PYSPARK_DRIVER_PYTHON"] = PYTHON_EXECUTABLE

# Disable native Hadoop Windows library
os.environ["HADOOP_OPTS"] = (
    os.environ.get("HADOOP_OPTS", "")
    + " -Dhadoop.native.lib=false"
)

os.environ["HADOOP_CLIENT_OPTS"] = (
    os.environ.get("HADOOP_CLIENT_OPTS", "")
    + " -Dhadoop.native.lib=false"
)

# ============================================================
# SPARK TEMP DIRECTORY
# ============================================================

SPARK_TEMP = r"D:\spark-temp"

os.makedirs(SPARK_TEMP, exist_ok=True)

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
    .appName("GoldDailyRevenue")
    .master("local[2]")

    # Windows / Hadoop
    .config(
        "spark.hadoop.fs.file.impl",
        "org.apache.hadoop.fs.RawLocalFileSystem"
    )
    .config(
        "spark.hadoop.fs.permissions.enabled",
        "false"
    )
    .config(
        "spark.hadoop.io.native.lib.available",
        "false"
    )
    .config(
        "spark.hadoop.hadoop.native.lib",
        "false"
    )
    .config(
        "spark.hadoop.fs.file.impl.disable.cache",
        "true"
    )

    # Python
    .config(
        "spark.pyspark.python",
        PYTHON_EXECUTABLE
    )
    .config(
        "spark.pyspark.driver.python",
        PYTHON_EXECUTABLE
    )

    # Temporary directory
    .config(
        "spark.local.dir",
        SPARK_TEMP
    )

    # Reduce resources
    .config(
        "spark.default.parallelism",
        "2"
    )
    .config(
        "spark.sql.shuffle.partitions",
        "2"
    )

    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("=" * 70)
print("CREATING GOLD - DAILY REVENUE")
print("=" * 70)

# ============================================================
# CHECK INPUT FILES
# ============================================================

if not os.path.exists(ORDERS_FILE):
    raise FileNotFoundError(
        f"Orders Silver file not found:\n{ORDERS_FILE}"
    )

if not os.path.exists(ORDER_ITEMS_FILE):
    raise FileNotFoundError(
        f"Order Items Silver file not found:\n{ORDER_ITEMS_FILE}"
    )

# ============================================================
# LOAD SILVER DATA
# ============================================================

print("\nLoading Silver orders...")

orders = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(ORDERS_FILE)
)

orders_count = orders.count()

print(f"Orders loaded: {orders_count}")

print("\nLoading Silver order items...")

order_items = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(ORDER_ITEMS_FILE)
)

order_items_count = order_items.count()

print(f"Order items loaded: {order_items_count}")

# ============================================================
# CONVERT TYPES
# ============================================================

orders = orders.withColumn(
    "order_date",
    F.to_timestamp("order_date")
)

order_items = order_items.withColumn(
    "line_total",
    F.col("line_total").cast("double")
)

# ============================================================
# JOIN ORDERS + ORDER ITEMS
# ============================================================

print("\nJoining orders and order items...")

revenue = order_items.join(
    orders.select(
        "order_id",
        "order_date",
        "region",
        "status"
    ),
    on="order_id",
    how="inner"
)

# ============================================================
# EXCLUDE CANCELLED ORDERS
# ============================================================

revenue = revenue.filter(
    F.lower(F.col("status")) != "cancelled"
)

# ============================================================
# CREATE DATE
# ============================================================

revenue = revenue.withColumn(
    "date",
    F.to_date("order_date")
)

# ============================================================
# DAILY REVENUE
# ============================================================

daily_revenue = (
    revenue
    .groupBy(
        "date",
        "region",
        "category"
    )
    .agg(
        F.round(
            F.sum("line_total"),
            2
        ).alias("total_revenue"),

        F.countDistinct(
            "order_id"
        ).alias("order_count")
    )
)

# ============================================================
# AVERAGE ORDER VALUE
# ============================================================

daily_revenue = daily_revenue.withColumn(
    "average_order_value",
    F.round(
        F.col("total_revenue")
        / F.col("order_count"),
        2
    )
)

# ============================================================
# WRITE TEMP CSV
# ============================================================

TEMP_DIR = os.path.join(
    GOLD_DIR,
    "daily_revenue_temp"
)

# Remove old temporary directory if present
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR, ignore_errors=True)

print("\nWriting Gold daily revenue...")

(
    daily_revenue
    .orderBy(
        "date",
        "region",
        "category"
    )
    .coalesce(1)
    .write
    .mode("overwrite")
    .option("header", "true")
    .csv(TEMP_DIR)
)

# ============================================================
# MOVE SINGLE CSV TO FINAL LOCATION
# ============================================================

csv_files = glob.glob(
    os.path.join(
        TEMP_DIR,
        "*.csv"
    )
)

if not csv_files:
    raise RuntimeError(
        "Gold daily revenue CSV was not created."
    )

if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

shutil.move(
    csv_files[0],
    OUTPUT_FILE
)

shutil.rmtree(
    TEMP_DIR,
    ignore_errors=True
)

# ============================================================
# SUMMARY
# ============================================================

row_count = daily_revenue.count()

total_revenue = (
    daily_revenue
    .agg(
        F.sum("total_revenue").alias("total")
    )
    .collect()[0]["total"]
)

total_orders = (
    daily_revenue
    .agg(
        F.sum("order_count").alias("total")
    )
    .collect()[0]["total"]
)

print("\n" + "=" * 70)
print("DAILY REVENUE CREATED SUCCESSFULLY")
print("=" * 70)

print(f"Output file: {OUTPUT_FILE}")
print(f"Gold rows: {row_count}")
print(f"Total revenue: {total_revenue:,.2f}")
print(f"Total orders: {total_orders:,}")

print("\nSample:")
daily_revenue.show(10, truncate=False)

print("\nStatus: SUCCESS")

# ============================================================
# STOP SPARK
# ============================================================

spark.stop()

print("\nSpark stopped successfully.")