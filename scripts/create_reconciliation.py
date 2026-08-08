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

GOLD_DIR = os.path.join(
    DATA_DIR,
    "gold"
)

os.makedirs(
    GOLD_DIR,
    exist_ok=True
)

# ============================================================
# DATASET FILES
# ============================================================

FILES = {
    "customers_bronze": os.path.join(
        DATA_DIR,
        "bronze",
        "customers",
        "customers_bronze.csv"
    ),

    "inventory_bronze": os.path.join(
        DATA_DIR,
        "bronze",
        "inventory",
        "inventory_bronze.csv"
    ),

    "orders_bronze": os.path.join(
        DATA_DIR,
        "bronze",
        "orders",
        "orders_bronze.csv"
    ),

    "order_items_bronze": os.path.join(
        DATA_DIR,
        "bronze",
        "order_items",
        "order_items_bronze.csv"
    ),

    "customers_silver": os.path.join(
        DATA_DIR,
        "silver",
        "customers",
        "customers_silver_validated.csv"
    ),

    "inventory_silver": os.path.join(
        DATA_DIR,
        "silver",
        "inventory",
        "inventory_silver_validated.csv"
    ),

    "orders_silver": os.path.join(
        DATA_DIR,
        "silver",
        "orders",
        "orders_silver_validated.csv"
    ),

    "order_items_silver": os.path.join(
        DATA_DIR,
        "silver",
        "order_items",
        "order_items_silver_validated.csv"
    ),

    "orders_quarantine": os.path.join(
        DATA_DIR,
        "quarantine",
        "orders",
        "orders",
        "orders_quarantine.csv"
    ),

    "order_items_quarantine": os.path.join(
        DATA_DIR,
        "quarantine",
        "order_items",
        "order_items",
        "order_items_quarantine.csv"
    ),

    "daily_revenue": os.path.join(
        GOLD_DIR,
        "daily_revenue.csv"
    ),

    "fulfillment_kpi": os.path.join(
        GOLD_DIR,
        "fulfillment_kpi.csv"
    ),

    "inventory_health": os.path.join(
        GOLD_DIR,
        "inventory_health.csv"
    ),

    "customer_ltv": os.path.join(
        GOLD_DIR,
        "customer_ltv.csv"
    )
}

# ============================================================
# COUNT CSV ROWS
# ============================================================

def count_csv_rows(path):

    if not os.path.exists(path):
        return None

    with open(
        path,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.reader(file)

        # Skip header
        next(reader, None)

        return sum(
            1 for _ in reader
        )


# ============================================================
# START
# ============================================================

print("=" * 70)
print("CREATING PIPELINE RECONCILIATION")
print("=" * 70)

captured_at = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

# ============================================================
# ROW COUNT RECONCILIATION
# ============================================================

print("\nCalculating row counts...")

row_counts = []

datasets = [
    ("bronze", "customers", "customers_bronze"),
    ("bronze", "inventory", "inventory_bronze"),
    ("bronze", "orders", "orders_bronze"),
    ("bronze", "order_items", "order_items_bronze"),

    ("silver", "customers", "customers_silver"),
    ("silver", "inventory", "inventory_silver"),
    ("silver", "orders", "orders_silver"),
    ("silver", "order_items", "order_items_silver"),

    ("gold", "daily_revenue", "daily_revenue"),
    ("gold", "fulfillment_kpi", "fulfillment_kpi"),
    ("gold", "inventory_health", "inventory_health"),
    ("gold", "customer_ltv", "customer_ltv")
]

for layer, table_name, file_key in datasets:

    path = FILES[file_key]

    count = count_csv_rows(path)

    if count is None:

        print(
            f"WARNING: File not found: {path}"
        )

        continue

    row_counts.append([
        captured_at,
        layer,
        table_name,
        count
    ])

    print(
        f"{layer:10} | "
        f"{table_name:20} | "
        f"{count:,}"
    )


# ============================================================
# WRITE ROW COUNT RECONCILIATION
# ============================================================

ROW_COUNT_FILE = os.path.join(
    GOLD_DIR,
    "reconciliation_row_counts.csv"
)

with open(
    ROW_COUNT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "captured_at",
        "layer",
        "table_name",
        "row_count"
    ])

    writer.writerows(
        row_counts
    )


# ============================================================
# DQ RECONCILIATION
# ============================================================

print("\nCreating DQ reconciliation...")

bronze_orders = count_csv_rows(
    FILES["orders_bronze"]
)

silver_orders = count_csv_rows(
    FILES["orders_silver"]
)

quarantine_orders = count_csv_rows(
    FILES["orders_quarantine"]
)

bronze_items = count_csv_rows(
    FILES["order_items_bronze"]
)

silver_items = count_csv_rows(
    FILES["order_items_silver"]
)

quarantine_items = count_csv_rows(
    FILES["order_items_quarantine"]
)

dq_summary = []


# ============================================================
# ORDERS DQ
# ============================================================

if bronze_orders is not None:

    if silver_orders is None:
        silver_orders = 0

    # If quarantine file is missing, calculate rejected
    # records from Bronze - Silver.
    if quarantine_orders is None:
        quarantine_orders = (
            bronze_orders - silver_orders
        )

    order_pass_rate = (
        silver_orders
        / bronze_orders
        * 100
    )

    order_quarantine_rate = (
        quarantine_orders
        / bronze_orders
        * 100
    )

    dq_summary.append([
        captured_at,
        "orders",
        bronze_orders,
        silver_orders,
        quarantine_orders,
        round(order_pass_rate, 2),
        round(order_quarantine_rate, 2)
    ])


# ============================================================
# ORDER ITEMS DQ
# ============================================================

if bronze_items is not None:

    if silver_items is None:
        silver_items = 0

    # If quarantine file is missing, calculate rejected
    # records from Bronze - Silver.
    if quarantine_items is None:
        quarantine_items = (
            bronze_items - silver_items
        )

    items_pass_rate = (
        silver_items
        / bronze_items
        * 100
    )

    items_quarantine_rate = (
        quarantine_items
        / bronze_items
        * 100
    )

    dq_summary.append([
        captured_at,
        "order_items",
        bronze_items,
        silver_items,
        quarantine_items,
        round(items_pass_rate, 2),
        round(items_quarantine_rate, 2)
    ])


# ============================================================
# WRITE DQ SUMMARY
# ============================================================

DQ_FILE = os.path.join(
    GOLD_DIR,
    "reconciliation_dq_summary.csv"
)

with open(
    DQ_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "captured_at",
        "dataset",
        "bronze_row_count",
        "silver_row_count",
        "quarantined_rows",
        "pass_rate_pct",
        "quarantine_rate_pct"
    ])

    writer.writerows(
        dq_summary
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("RECONCILIATION CREATED SUCCESSFULLY")
print("=" * 70)

print(
    f"\nRow count file:"
    f"\n{ROW_COUNT_FILE}"
)

print(
    f"\nDQ summary file:"
    f"\n{DQ_FILE}"
)

print("\nDQ Summary")
print("-" * 70)

for row in dq_summary:

    print(
        f"{row[1]:15} | "
        f"Bronze: {row[2]:,} | "
        f"Silver: {row[3]:,} | "
        f"Quarantine: {row[4]:,} | "
        f"Pass: {row[5]:.2f}% | "
        f"Quarantine: {row[6]:.2f}%"
    )

print("\nStatus: SUCCESS")