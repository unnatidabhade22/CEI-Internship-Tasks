import os
import sys
import csv

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(PROJECT_ROOT)

from config import DATA_DIR

# ============================================================
# PATHS
# ============================================================

SILVER_DIR = os.path.join(DATA_DIR, "silver")
QUARANTINE_DIR = os.path.join(DATA_DIR, "quarantine")


# ============================================================
# HELPERS
# ============================================================

def load_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if not rows:
        # Create an empty file if there are no rows
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("")
        return

    fieldnames = list(rows[0].keys())

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(rows)


def get_value(row, column):
    value = row.get(column, "")
    if value is None:
        return ""
    return str(value).strip()


# ============================================================
# LOAD VALIDATED SILVER DATA
# ============================================================

customers_path = os.path.join(
    SILVER_DIR,
    "customers",
    "customers_silver_validated.csv"
)

inventory_path = os.path.join(
    SILVER_DIR,
    "inventory",
    "inventory_silver_validated.csv"
)

orders_path = os.path.join(
    SILVER_DIR,
    "orders",
    "orders_silver_validated.csv"
)

order_items_path = os.path.join(
    SILVER_DIR,
    "order_items",
    "order_items_silver_validated.csv"
)

customers = load_csv(customers_path)
inventory = load_csv(inventory_path)
orders = load_csv(orders_path)
order_items = load_csv(order_items_path)


print("=" * 70)
print("REFERENTIAL INTEGRITY VALIDATION")
print("=" * 70)

print()
print("Loaded validated Silver datasets:")
print("Customers:", len(customers))
print("Inventory:", len(inventory))
print("Orders:", len(orders))
print("Order Items:", len(order_items))


# ============================================================
# 1. ORDERS -> CUSTOMERS
# ============================================================

valid_customer_ids = {
    get_value(row, "customer_id")
    for row in customers
    if get_value(row, "customer_id")
}

orders_valid = []
orders_invalid = []

for row in orders:

    customer_id = get_value(row, "customer_id")

    if customer_id not in valid_customer_ids:
        row["quarantine_reason"] = (
            "Customer ID not found in customers"
        )
        orders_invalid.append(row)
    else:
        orders_valid.append(row)


# ============================================================
# 2. ORDER ITEMS -> ORDERS
# ============================================================

valid_order_ids = {
    get_value(row, "order_id")
    for row in orders_valid
    if get_value(row, "order_id")
}

order_items_valid = []
order_items_invalid_order = []

for row in order_items:

    order_id = get_value(row, "order_id")

    if order_id not in valid_order_ids:
        row["quarantine_reason"] = (
            "Order ID not found in orders"
        )
        order_items_invalid_order.append(row)
    else:
        order_items_valid.append(row)


# ============================================================
# 3. ORDER ITEMS -> INVENTORY
# ============================================================

valid_sku_ids = {
    get_value(row, "sku_id")
    for row in inventory
    if get_value(row, "sku_id")
}

order_items_final = []
order_items_invalid_sku = []

for row in order_items_valid:

    sku_id = get_value(row, "sku_id")

    if sku_id not in valid_sku_ids:
        row["quarantine_reason"] = (
            "SKU ID not found in inventory"
        )
        order_items_invalid_sku.append(row)
    else:
        order_items_final.append(row)


# ============================================================
# SAVE QUARANTINE FILES
# ============================================================

orders_reference_path = os.path.join(
    QUARANTINE_DIR,
    "orders",
    "orders_reference_quarantine.csv"
)

save_csv(
    orders_reference_path,
    orders_invalid
)


order_items_order_path = os.path.join(
    QUARANTINE_DIR,
    "order_items",
    "order_items_order_reference_quarantine.csv"
)

save_csv(
    order_items_order_path,
    order_items_invalid_order
)


order_items_sku_path = os.path.join(
    QUARANTINE_DIR,
    "order_items",
    "order_items_sku_reference_quarantine.csv"
)

save_csv(
    order_items_sku_path,
    order_items_invalid_sku
)


# ============================================================
# SAVE FINAL REFERENTIALLY VALID DATA
# ============================================================

orders_final_path = os.path.join(
    SILVER_DIR,
    "orders",
    "orders_silver_final.csv"
)

save_csv(
    orders_final_path,
    orders_valid
)


order_items_final_path = os.path.join(
    SILVER_DIR,
    "order_items",
    "order_items_silver_final.csv"
)

save_csv(
    order_items_final_path,
    order_items_final
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("ORDERS -> CUSTOMERS")
print("-" * 50)
print("Input orders:", len(orders))
print("Valid orders:", len(orders_valid))
print("Invalid customer references:", len(orders_invalid))

print()
print("ORDER ITEMS -> ORDERS")
print("-" * 50)
print(
    "Invalid order references:",
    len(order_items_invalid_order)
)

print()
print("ORDER ITEMS -> INVENTORY")
print("-" * 50)
print(
    "Invalid SKU references:",
    len(order_items_invalid_sku)
)

print()
print("FINAL REFERENTIALLY VALID RECORDS")
print("-" * 50)
print("Orders:", len(orders_valid))
print("Order Items:", len(order_items_final))

print()
print("=" * 70)
print("REFERENTIAL INTEGRITY VALIDATION COMPLETED SUCCESSFULLY!")
print("=" * 70)