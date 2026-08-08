import os
import sys
import csv
from datetime import datetime

# ============================================================
# ADD PROJECT ROOT TO PYTHON PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(PROJECT_ROOT)

from config import DATA_DIR

# ============================================================
# PATHS
# ============================================================

LANDING_DIR = os.path.join(DATA_DIR, "landing")
BRONZE_DIR = os.path.join(DATA_DIR, "bronze")

# ============================================================
# DATASETS
# ============================================================

datasets = [
    "customers",
    "inventory",
    "orders",
    "order_items"
]

# ============================================================
# BRONZE INGESTION TIMESTAMP
# ============================================================

bronze_timestamp = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

load_date = datetime.now().strftime(
    "%Y-%m-%d"
)

# ============================================================
# CREATE BRONZE LAYER
# ============================================================

print("=" * 70)
print("BRONZE LAYER CREATION")
print("=" * 70)

for dataset in datasets:

    landing_file = os.path.join(
        LANDING_DIR,
        dataset,
        f"{dataset}.csv"
    )

    bronze_dataset_dir = os.path.join(
        BRONZE_DIR,
        dataset
    )

    os.makedirs(
        bronze_dataset_dir,
        exist_ok=True
    )

    bronze_file = os.path.join(
        bronze_dataset_dir,
        f"{dataset}_bronze.csv"
    )

    # --------------------------------------------------------
    # Check source file
    # --------------------------------------------------------

    if not os.path.exists(landing_file):

        print("\nERROR: Landing file not found:")
        print(landing_file)

        continue

    # --------------------------------------------------------
    # Read Landing data
    # --------------------------------------------------------

    with open(
        landing_file,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as infile:

        reader = csv.DictReader(infile)

        rows = list(reader)

        fieldnames = list(reader.fieldnames)

    # --------------------------------------------------------
    # Add Bronze metadata
    # --------------------------------------------------------

    fieldnames.extend([
        "bronze_ingestion_timestamp",
        "source_file_name",
        "load_date"
    ])

    source_file_name = os.path.basename(
        landing_file
    )

    for row in rows:

        row["bronze_ingestion_timestamp"] = bronze_timestamp
        row["source_file_name"] = source_file_name
        row["load_date"] = load_date

    # --------------------------------------------------------
    # Save Bronze data
    # --------------------------------------------------------

    with open(
        bronze_file,
        "w",
        encoding="utf-8",
        newline=""
    ) as outfile:

        writer = csv.DictWriter(
            outfile,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print(f"\nDataset: {dataset}")
    print(f"Input rows: {len(rows)}")
    print(f"Bronze file: {bronze_file}")
    print("Status: SUCCESS")


print("\n" + "=" * 70)
print("Bronze layer created successfully!")
print("=" * 70)