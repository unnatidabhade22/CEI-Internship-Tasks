import os
import sys
import csv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from config import DATA_DIR

SILVER_DIR = os.path.join(DATA_DIR, "silver")
QUARANTINE_DIR = os.path.join(DATA_DIR, "quarantine")

DATASETS = ["customers", "inventory", "orders", "order_items"]

for dataset in DATASETS:
    os.makedirs(os.path.join(QUARANTINE_DIR, dataset), exist_ok=True)


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    if not rows:
        return

    os.makedirs(os.path.dirname(path), exist_ok=True)

    fieldnames = list(rows[0].keys())

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def blank(value):
    return value is None or str(value).strip() == ""


def number(value):
    if blank(value):
        return None
    try:
        return float(str(value).strip())
    except:
        return None


def validate(dataset, rows, invalid_function):
    valid = []
    quarantine = []

    for row in rows:
        reason = invalid_function(row)

        if reason:
            row["quarantine_reason"] = reason
            quarantine.append(row)
        else:
            valid.append(row)

    validated_path = os.path.join(
        SILVER_DIR,
        dataset,
        f"{dataset}_silver_validated.csv"
    )

    quarantine_path = os.path.join(
        QUARANTINE_DIR,
        dataset,
        f"{dataset}_quarantine.csv"
    )

    write_csv(validated_path, valid)
    write_csv(quarantine_path, quarantine)

    print()
    print(f"Dataset: {dataset}")
    print(f"Valid records: {len(valid)}")
    print(f"Quarantined records: {len(quarantine)}")
    print(f"Valid file: {validated_path}")
    print(f"Quarantine file: {quarantine_path}")

    return valid, quarantine


print("=" * 70)
print("DATA QUALITY VALIDATION AND QUARANTINE")
print("=" * 70)


customers = read_csv(os.path.join(
    SILVER_DIR, "customers", "customers_silver.csv"
))

inventory = read_csv(os.path.join(
    SILVER_DIR, "inventory", "inventory_silver.csv"
))

orders = read_csv(os.path.join(
    SILVER_DIR, "orders", "orders_silver.csv"
))

order_items = read_csv(os.path.join(
    SILVER_DIR, "order_items", "order_items_silver.csv"
))


def customer_rule(row):
    if blank(row.get("customer_id")):
        return "Missing customer_id"
    return ""


def inventory_rule(row):
    value = number(row.get("stock_quantity"))

    if value is None:
        return "Missing stock_quantity"

    if value < 0:
        return "Negative stock_quantity"

    return ""


def orders_rule(row):
    if blank(row.get("order_id")):
        return "Missing order_id"

    if blank(row.get("customer_id")):
        return "Missing customer_id"

    if blank(row.get("order_date")):
        return "Invalid order_date"

    amount = number(row.get("total_amount"))

    if amount is not None and amount < 0:
        return "Negative total_amount"

    return ""


def order_items_rule(row):
    if blank(row.get("item_id")):
        return "Missing item_id"

    if blank(row.get("order_id")):
        return "Missing order_id"

    if blank(row.get("sku_id")):
        return "Missing sku_id"

    quantity = number(row.get("quantity"))

    if quantity is None:
        return "Missing quantity"

    if quantity <= 0:
        return "Invalid quantity"

    unit_price = number(row.get("unit_price"))

    if unit_price is None:
        return "Missing unit_price"

    if unit_price < 0:
        return "Negative unit_price"

    if blank(row.get("line_total")):
        return "Missing line_total"

    return ""


results = {}

results["customers"] = validate(
    "customers",
    customers,
    customer_rule
)

results["inventory"] = validate(
    "inventory",
    inventory,
    inventory_rule
)

results["orders"] = validate(
    "orders",
    orders,
    orders_rule
)

results["order_items"] = validate(
    "order_items",
    order_items,
    order_items_rule
)


print()
print("=" * 70)
print("DATA QUALITY SUMMARY")
print("=" * 70)

for dataset in DATASETS:
    valid, quarantine = results[dataset]
    total = len(valid) + len(quarantine)

    percentage = (
        (len(valid) / total) * 100
        if total else 0
    )

    print(
        f"{dataset:15} "
        f"Input: {total:6}  "
        f"Valid: {len(valid):6}  "
        f"Quarantine: {len(quarantine):6}  "
        f"Valid %: {percentage:.2f}"
    )

print()
print("=" * 70)
print("Data quality validation completed successfully!")
print("=" * 70)
