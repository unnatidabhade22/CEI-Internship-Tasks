import os

# Disable Hadoop Windows permission requirement
os.environ["HADOOP_HOME"] = os.getcwd()
os.environ["hadoop.home.dir"] = os.getcwd()

from pyspark.sql import SparkSession


spark = (
    SparkSession.builder
    .appName("SparkEnvironmentTest")
    .master("local[*]")
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")
    .config("spark.hadoop.fs.permissions.enabled", "false")
    .getOrCreate()
)

print("=" * 60)
print("SPARK ENVIRONMENT TEST")
print("=" * 60)

print("Spark version:", spark.version)

test_df = spark.createDataFrame(
    [
        (1, "Test"),
        (2, "Spark"),
        (3, "Delta")
    ],
    ["id", "name"]
)

print("\nTest Data:")
test_df.show()

print("Spark is working successfully!")

spark.stop()