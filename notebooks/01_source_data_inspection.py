import pandas as pd
import os

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "data", "source")

# Dataset paths
customers_path = os.path.join(SOURCE_DIR, "customers.csv")
inventory_path = os.path.join(SOURCE_DIR, "inventory.csv")
orders_path = os.path.join(SOURCE_DIR, "orders.csv")
order_items_path = os.path.join(SOURCE_DIR, "order_items.csv")

# Load source datasets
customers = pd.read_csv(customers_path)
inventory = pd.read_csv(inventory_path)
orders = pd.read_csv(orders_path)
order_items = pd.read_csv(order_items_path)

print("Source datasets loaded successfully!\n")

# Display basic information
datasets = {
    "Customers": customers,
    "Inventory": inventory,
    "Orders": orders,
    "Order Items": order_items
}

for name, df in datasets.items():
    print("=" * 60)
    print(name)
    print("=" * 60)
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Column Names:", list(df.columns))
    print()

    # ============================================================
# SOURCE DATA QUALITY PROFILING
# ============================================================

print("\n\nSOURCE DATA QUALITY REPORT")
print("=" * 70)

for name, df in datasets.items():

    print(f"\n{name}")
    print("-" * 70)

    # Row and column count
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    # Missing values
    print("\nMissing Values:")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.sum() > 0 else "No missing values found")

    # Duplicate rows
    duplicate_count = df.duplicated().sum()
    print("\nDuplicate Rows:", duplicate_count)

    # Data types
    print("\nData Types:")
    print(df.dtypes)

print("\nSource data profiling completed successfully!")