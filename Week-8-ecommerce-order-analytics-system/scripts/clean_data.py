import pandas as pd
import os

# ----------------------------------------
# Project Paths
# ----------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned")

os.makedirs(CLEAN_DATA_PATH, exist_ok=True)

# ----------------------------------------
# Load Raw Datasets
# ----------------------------------------

customers = pd.read_csv(os.path.join(RAW_DATA_PATH, "customers.csv"))
products = pd.read_csv(os.path.join(RAW_DATA_PATH, "products.csv"))
orders = pd.read_csv(os.path.join(RAW_DATA_PATH, "orders.csv"))
order_items = pd.read_csv(os.path.join(RAW_DATA_PATH, "order_items.csv"))

print("All datasets loaded successfully!\n")

# =====================================================
# Clean Customers
# =====================================================

print("Cleaning Customers...")

customers["email"] = customers["email"].fillna("unknown@email.com")

customers["join_date"] = pd.to_datetime(
    customers["join_date"],
    errors="coerce"
)

today = pd.Timestamp.today()

customers.loc[
    customers["join_date"] > today,
    "join_date"
] = today

customers = customers.drop_duplicates()

print("Customers cleaned successfully.")

# =====================================================
# Clean Products
# =====================================================

print("\nCleaning Products...")

products["price"] = products["price"].fillna(
    products["price"].median()
)

products.loc[
    products["stock"] < 0,
    "stock"
] = 0

products = products.drop_duplicates()

print("Products cleaned successfully.")

# =====================================================
# Clean Orders
# =====================================================

print("\nCleaning Orders...")

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

orders.loc[
    orders["order_date"] > today,
    "order_date"
] = today

orders = orders.drop_duplicates()

print("Orders cleaned successfully.")

# =====================================================
# Clean Order Items
# =====================================================

print("\nCleaning Order Items...")

order_items["quantity"] = order_items["quantity"].fillna(1)

order_items = order_items.drop_duplicates()

print("Order Items cleaned successfully.")

# =====================================================
# Referential Integrity Checks
# =====================================================

print("\nValidating Relationships...")

valid_customers = set(customers["customer_id"])

orders = orders[
    orders["customer_id"].isin(valid_customers)
]

valid_products = set(products["product_id"])

order_items = order_items[
    order_items["product_id"].isin(valid_products)
]

valid_orders = set(orders["order_id"])

order_items = order_items[
    order_items["order_id"].isin(valid_orders)
]

print("Referential integrity validated successfully.")

# =====================================================
# Save Cleaned Files
# =====================================================

customers.to_csv(
    os.path.join(CLEAN_DATA_PATH, "customers_clean.csv"),
    index=False
)

products.to_csv(
    os.path.join(CLEAN_DATA_PATH, "products_clean.csv"),
    index=False
)

orders.to_csv(
    os.path.join(CLEAN_DATA_PATH, "orders_clean.csv"),
    index=False
)

order_items.to_csv(
    os.path.join(CLEAN_DATA_PATH, "order_items_clean.csv"),
    index=False
)

print("\nAll cleaned datasets saved successfully!")

# =====================================================
# Summary
# =====================================================

print("\nFinal Dataset Shapes")

print("Customers :", customers.shape)
print("Products  :", products.shape)
print("Orders    :", orders.shape)
print("OrderItems:", order_items.shape)