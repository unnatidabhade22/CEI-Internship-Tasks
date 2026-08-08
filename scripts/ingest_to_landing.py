import os
import shutil
import sys
from datetime import datetime

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(PROJECT_ROOT)

from config import (
    SOURCE_DIR,
    DATA_DIR,
    CUSTOMERS_FILE,
    INVENTORY_FILE,
    ORDERS_FILE,
    ORDER_ITEMS_FILE
)

# ============================================================
# LANDING INGESTION
# ============================================================

LANDING_DIR = os.path.join(DATA_DIR, "landing")

datasets = {
    "customers": CUSTOMERS_FILE,
    "inventory": INVENTORY_FILE,
    "orders": ORDERS_FILE,
    "order_items": ORDER_ITEMS_FILE
}

# Create landing directories
for dataset_name in datasets:
    os.makedirs(
        os.path.join(LANDING_DIR, dataset_name),
        exist_ok=True
    )

# Ingestion timestamp
ingestion_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("=" * 70)
print("LANDING LAYER INGESTION")
print("=" * 70)

for dataset_name, source_file in datasets.items():

    if not os.path.exists(source_file):
        print(f"ERROR: Source file not found: {source_file}")
        continue

    landing_dataset_dir = os.path.join(
        LANDING_DIR,
        dataset_name
    )

    file_name = os.path.basename(source_file)

    destination_file = os.path.join(
        landing_dataset_dir,
        file_name
    )

    # Copy source file to landing
    shutil.copy2(
        source_file,
        destination_file
    )

    print(f"\nDataset: {dataset_name}")
    print(f"Source: {source_file}")
    print(f"Landing: {destination_file}")
    print(f"Ingestion Time: {ingestion_timestamp}")
    print("Status: SUCCESS")

print("\n" + "=" * 70)
print("Landing layer ingestion completed successfully!")
print("=" * 70)