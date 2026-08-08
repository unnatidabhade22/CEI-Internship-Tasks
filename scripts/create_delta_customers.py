import os
import sys
import shutil

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SOURCE_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "source"
)

SILVER_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "silver",
    "customers",
    "customers_silver_validated.csv"
)

# IMPORTANT:
# Delta is stored outside OneDrive to avoid Windows file-locking
# problems with _delta_log/_staged_commits.
DELTA_PATH = r"D:\ecommerce-delta\customers"

# ============================================================
# WINDOWS HADOOP
# ============================================================

HADOOP_HOME = PROJECT_ROOT

os.environ["HADOOP_HOME"] = HADOOP_HOME
os.environ["hadoop.home.dir"] = HADOOP_HOME

WINUTILS = os.path.join(
    HADOOP_HOME,
    "bin",
    "winutils.exe"
)

if not os.path.exists(WINUTILS):
    raise FileNotFoundError(
        f"winutils.exe not found at:\n{WINUTILS}"
    )

os.environ["PATH"] = (
    os.path.join(HADOOP_HOME, "bin")
    + os.pathsep
    + os.environ.get("PATH", "")
)

# ============================================================
# PYTHON
# ============================================================

PYTHON_EXECUTABLE = sys.executable

os.environ["PYSPARK_PYTHON"] = PYTHON_EXECUTABLE
os.environ["PYSPARK_DRIVER_PYTHON"] = PYTHON_EXECUTABLE

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
# DISABLE HADOOP NATIVE LIBRARY
# ============================================================

os.environ["HADOOP_OPTS"] = (
    os.environ.get("HADOOP_OPTS", "")
    + " -Dhadoop.native.lib=false"
)

os.environ["HADOOP_CLIENT_OPTS"] = (
    os.environ.get("HADOOP_CLIENT_OPTS", "")
    + " -Dhadoop.native.lib=false"
)

# ============================================================
# PROJECT INFORMATION
# ============================================================

print("Project configuration loaded successfully!")
print("Project: E-Commerce Data Engineering Pipeline")
print(f"Project root: {PROJECT_ROOT}")
print(f"Source directory: {SOURCE_DIR}")

print("=" * 70)
print("CHECKING WINDOWS HADOOP")
print("=" * 70)

print(f"HADOOP_HOME: {HADOOP_HOME}")
print(f"winutils.exe: {WINUTILS}")

print("winutils.exe found successfully!")
print(f"Spark temporary directory: {SPARK_TEMP}")

# ============================================================
# CHECK SILVER FILE
# ============================================================

print()
print("=" * 70)
print("CHECKING SILVER CUSTOMERS")
print("=" * 70)

print(f"Silver file: {SILVER_FILE}")

if not os.path.exists(SILVER_FILE):
    raise FileNotFoundError(
        f"Silver customers file not found:\n{SILVER_FILE}"
    )

print("Silver customers file found successfully!")

# ============================================================
# START SPARK + DELTA
# ============================================================

print()
print("=" * 70)
print("STARTING SPARK + DELTA")
print("=" * 70)

from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder

    .appName("EcommerceDeltaCustomers")

    .master("local[2]")

    # ========================================================
    # DELTA LAKE
    # ========================================================

    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    )

    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )

    # Use ONE Delta LogStore configuration only.
    .config(
        "spark.delta.logStore.class",
        "org.apache.spark.sql.delta.storage.LocalLogStore"
    )

    # ========================================================
    # WINDOWS / HADOOP
    # ========================================================

    .config(
        "spark.hadoop.fs.file.impl",
        "org.apache.hadoop.fs.LocalFileSystem"
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

    # ========================================================
    # PYTHON
    # ========================================================

    .config(
        "spark.pyspark.python",
        PYTHON_EXECUTABLE
    )

    .config(
        "spark.pyspark.driver.python",
        PYTHON_EXECUTABLE
    )

    # ========================================================
    # SPARK TEMP
    # ========================================================

    .config(
        "spark.local.dir",
        SPARK_TEMP
    )

    # ========================================================
    # PERFORMANCE
    # ========================================================

    .config(
        "spark.default.parallelism",
        "2"
    )

    .config(
        "spark.sql.shuffle.partitions",
        "2"
    )
)

spark = None

try:

    spark = (
        configure_spark_with_delta_pip(builder)
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    print(f"Spark version: {spark.version}")
    print(f"Python executable: {PYTHON_EXECUTABLE}")
    print(f"HADOOP_HOME: {HADOOP_HOME}")

    # ========================================================
    # VERIFY CONFIGURATION
    # ========================================================

    print()
    print("=" * 70)
    print("VERIFYING SPARK / HADOOP / DELTA CONFIGURATION")
    print("=" * 70)

    hadoop_conf = (
        spark.sparkContext
        ._jsc
        .hadoopConfiguration()
    )

    print(
        "fs.file.impl:",
        hadoop_conf.get("fs.file.impl")
    )

    print(
        "fs.permissions.enabled:",
        hadoop_conf.get("fs.permissions.enabled")
    )

    print(
        "io.native.lib.available:",
        hadoop_conf.get("io.native.lib.available")
    )

    print(
        "hadoop.native.lib:",
        hadoop_conf.get("hadoop.native.lib")
    )

    print(
        "fs.file.impl.disable.cache:",
        hadoop_conf.get("fs.file.impl.disable.cache")
    )

    print(
        "Delta log store:",
        spark.conf.get(
            "spark.delta.logStore.class",
            "NOT SET"
        )
    )

    # ========================================================
    # LOAD SILVER CUSTOMERS
    # ========================================================

    print()
    print("=" * 70)
    print("LOADING VALIDATED SILVER CUSTOMERS")
    print("=" * 70)

    customers_df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(SILVER_FILE)
    )

    print("Customers loaded successfully!")

    row_count = customers_df.count()

    print(f"Customer rows: {row_count}")

    if row_count == 0:
        raise RuntimeError(
            "Silver customers contains zero rows."
        )

    print(
        "Customer row count validation: PASSED"
    )

    print()
    print("Customer schema:")

    customers_df.printSchema()

    # ========================================================
    # PREPARE DELTA DIRECTORY
    # ========================================================

    print()
    print("=" * 70)
    print("PREPARING DELTA LOCATION")
    print("=" * 70)

    print(f"Delta path: {DELTA_PATH}")

    # Ensure parent directory exists.
    os.makedirs(
        os.path.dirname(DELTA_PATH),
        exist_ok=True
    )

    # Remove previous failed/incomplete Delta table.
    if os.path.exists(DELTA_PATH):

        print(
            "Existing Delta directory found."
        )

        print(
            "Removing previous Delta table..."
        )

        shutil.rmtree(
            DELTA_PATH
        )

        print(
            "Previous Delta directory removed."
        )

    os.makedirs(
        DELTA_PATH,
        exist_ok=True
    )

    print(
        "Delta directory prepared successfully."
    )

    # ========================================================
    # WRITE DELTA
    # ========================================================

    print()
    print("=" * 70)
    print("WRITING CUSTOMERS TO DELTA")
    print("=" * 70)

    (
        customers_df
        .write
        .format("delta")
        .mode("overwrite")
        .option(
            "overwriteSchema",
            "true"
        )
        .save(DELTA_PATH)
    )

    print()
    print("=" * 70)
    print("DELTA TABLE CREATED SUCCESSFULLY!")
    print("=" * 70)

    print(f"Delta location: {DELTA_PATH}")

    # ========================================================
    # VERIFY DELTA DIRECTORY
    # ========================================================

    print()
    print("=" * 70)
    print("VERIFYING DELTA TABLE")
    print("=" * 70)

    if not os.path.exists(DELTA_PATH):
        raise RuntimeError(
            "Delta directory was not created."
        )

    DELTA_LOG = os.path.join(
        DELTA_PATH,
        "_delta_log"
    )

    if not os.path.exists(DELTA_LOG):
        raise RuntimeError(
            "Delta _delta_log directory was not created."
        )

    print("Delta directory: FOUND")
    print("Delta transaction log: FOUND")

    # ========================================================
    # FIND DELTA FILES
    # ========================================================

    delta_files = []

    for root, dirs, files in os.walk(DELTA_PATH):

        for file in files:

            full_path = os.path.join(
                root,
                file
            )

            delta_files.append(full_path)

    parquet_files = [
        file
        for file in delta_files
        if file.lower().endswith(".parquet")
    ]

    json_files = [
        file
        for file in delta_files
        if file.lower().endswith(".json")
    ]

    print(
        f"Delta files: {len(delta_files)}"
    )

    print(
        f"Parquet files: {len(parquet_files)}"
    )

    print(
        f"JSON transaction files: {len(json_files)}"
    )

    if len(parquet_files) == 0:
        raise RuntimeError(
            "No Parquet data files were created."
        )

    if len(json_files) == 0:
        raise RuntimeError(
            "No Delta transaction log JSON files were created."
        )

    print(
        "Delta file validation: PASSED"
    )

    # ========================================================
    # READ DELTA TABLE BACK
    # ========================================================

    print()
    print("=" * 70)
    print("READING DELTA TABLE BACK")
    print("=" * 70)

    delta_df = (
        spark.read
        .format("delta")
        .load(DELTA_PATH)
    )

    delta_row_count = delta_df.count()

    print(
        f"Silver rows: {row_count}"
    )

    print(
        f"Delta rows: {delta_row_count}"
    )

    # ========================================================
    # ROW COUNT VALIDATION
    # ========================================================

    if delta_row_count != row_count:

        raise RuntimeError(
            "Silver -> Delta row count validation FAILED.\n"
            f"Silver rows: {row_count}\n"
            f"Delta rows: {delta_row_count}"
        )

    print(
        "Silver -> Delta row count validation: PASSED"
    )

    # ========================================================
    # READ-BACK SCHEMA
    # ========================================================

    print()
    print("Delta schema:")

    delta_df.printSchema()

    print(
        "Delta read-back: SUCCESSFUL"
    )

    # ========================================================
    # FINAL SUCCESS
    # ========================================================

    print()
    print("=" * 70)
    print("FINAL DELTA VALIDATION")
    print("=" * 70)

    print("Silver customers : VALID")
    print("Delta directory  : VALID")
    print("Delta log        : VALID")
    print("Parquet data     : VALID")
    print("Delta read-back  : VALID")
    print("Row count        : MATCHED")

    print()
    print("=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("Delta table       : CREATED SUCCESSFULLY")
    print("Delta read-back   : SUCCESSFUL")
    print("Status            : SUCCESS")

except Exception as e:

    print()
    print("=" * 70)
    print("PIPELINE FAILED")
    print("=" * 70)

    print(f"Error: {e}")

    raise

finally:

    if spark is not None:

        spark.stop()

        print()
        print("Spark stopped successfully.")