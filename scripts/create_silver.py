import os
import sys
import pandas as pd

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

BRONZE_DIR = os.path.join(DATA_DIR, "bronze")
SILVER_DIR = os.path.join(DATA_DIR, "silver")


# ============================================================
# CREATE SILVER DIRECTORIES
# ============================================================

for dataset in [
    "customers",
    "inventory",
    "orders",
    "order_items"
]:
    os.makedirs(
        os.path.join(SILVER_DIR, dataset),
        exist_ok=True
    )


# ============================================================
# HELPER FUNCTION
# ============================================================

def save_silver(df, dataset):

    output_path = os.path.join(
        SILVER_DIR,
        dataset,
        f"{dataset}_silver.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(f"{dataset}: Silver file created")
    print(f"Rows: {len(df)}")
    print(f"Location: {output_path}")
    print("-" * 60)


# ============================================================
# LOAD BRONZE DATA
# ============================================================

customers = pd.read_csv(
    os.path.join(
        BRONZE_DIR,
        "customers",
        "customers_bronze.csv"
    )
)

inventory = pd.read_csv(
    os.path.join(
        BRONZE_DIR,
        "inventory",
        "inventory_bronze.csv"
    )
)

orders = pd.read_csv(
    os.path.join(
        BRONZE_DIR,
        "orders",
        "orders_bronze.csv"
    )
)

order_items = pd.read_csv(
    os.path.join(
        BRONZE_DIR,
        "order_items",
        "order_items_bronze.csv"
    )
)


print("=" * 70)
print("SILVER LAYER DATA CLEANING")
print("=" * 70)


# ============================================================
# 1. CUSTOMERS CLEANING
# ============================================================

print("\nCleaning Customers...")

# Remove duplicate customer records
customers = customers.drop_duplicates(
    subset=["customer_id"]
)

# Convert signup date
customers["signup_date"] = pd.to_datetime(
    customers["signup_date"],
    errors="coerce"
)

# Convert active flag to integer
customers["is_active"] = pd.to_numeric(
    customers["is_active"],
    errors="coerce"
).fillna(0).astype(int)

# Clean email
customers["email"] = (
    customers["email"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# Remove unnecessary whitespace
for column in [
    "first_name",
    "last_name",
    "city",
    "state",
    "region"
]:
    customers[column] = (
        customers[column]
        .astype(str)
        .str.strip()
    )


# ============================================================
# 2. INVENTORY CLEANING
# ============================================================

print("Cleaning Inventory...")

# Remove duplicate SKU records
inventory = inventory.drop_duplicates(
    subset=["sku_id", "warehouse_id"]
)

# Convert numeric columns
inventory["stock_quantity"] = pd.to_numeric(
    inventory["stock_quantity"],
    errors="coerce"
)

inventory["reorder_level"] = pd.to_numeric(
    inventory["reorder_level"],
    errors="coerce"
)

inventory["unit_cost"] = pd.to_numeric(
    inventory["unit_cost"],
    errors="coerce"
)

# Fill missing stock quantity with zero
inventory["stock_quantity"] = (
    inventory["stock_quantity"]
    .fillna(0)
)

# Convert date
inventory["last_updated"] = pd.to_datetime(
    inventory["last_updated"],
    errors="coerce"
)


# ============================================================
# 3. ORDERS CLEANING
# ============================================================

print("Cleaning Orders...")

# Remove duplicate order records
orders = orders.drop_duplicates(
    subset=["order_id"],
    keep="first"
)

# Convert date
orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

# Convert numeric columns
orders["total_amount"] = pd.to_numeric(
    orders["total_amount"],
    errors="coerce"
)

orders["discount_amount"] = pd.to_numeric(
    orders["discount_amount"],
    errors="coerce"
)

# Clean text fields
for column in [
    "order_id",
    "customer_id",
    "status",
    "payment_method",
    "warehouse_id",
    "region"
]:
    orders[column] = (
        orders[column]
        .astype("string")
        .str.strip()
    )


# ============================================================
# 4. ORDER ITEMS CLEANING
# ============================================================

print("Cleaning Order Items...")

# Remove duplicate item records
order_items = order_items.drop_duplicates(
    subset=["item_id"]
)

# Convert numeric fields
order_items["quantity"] = pd.to_numeric(
    order_items["quantity"],
    errors="coerce"
)

order_items["unit_price"] = pd.to_numeric(
    order_items["unit_price"],
    errors="coerce"
)

order_items["line_total"] = pd.to_numeric(
    order_items["line_total"],
    errors="coerce"
)

# Recalculate missing line totals
missing_line_total = (
    order_items["line_total"].isna()
)

order_items.loc[
    missing_line_total,
    "line_total"
] = (
    order_items.loc[
        missing_line_total,
        "quantity"
    ]
    *
    order_items.loc[
        missing_line_total,
        "unit_price"
    ]
)

# Clean text columns
for column in [
    "item_id",
    "order_id",
    "sku_id",
    "product_name",
    "category"
]:
    order_items[column] = (
        order_items[column]
        .astype("string")
        .str.strip()
    )


# ============================================================
# 5. SAVE SILVER DATA
# ============================================================

print("\nSaving Silver datasets...")
print("=" * 70)

save_silver(
    customers,
    "customers"
)

save_silver(
    inventory,
    "inventory"
)

save_silver(
    orders,
    "orders"
)

save_silver(
    order_items,
    "order_items"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SILVER LAYER CREATED SUCCESSFULLY!")
print("=" * 70)

print("\nFinal Silver Row Counts:")
print("Customers:", len(customers))
print("Inventory:", len(inventory))
print("Orders:", len(orders))
print("Order Items:", len(order_items))