import os

# ============================================================
# PROJECT CONFIGURATION
# ============================================================

# Project root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# LOCAL DATA PATHS
# ============================================================

DATA_DIR = os.path.join(BASE_DIR, "data")

SOURCE_DIR = os.path.join(DATA_DIR, "source")

INCREMENTAL_DIR = os.path.join(DATA_DIR, "incremental")

# ============================================================
# PROJECT OUTPUT PATHS
# ============================================================

NOTEBOOK_DIR = os.path.join(BASE_DIR, "notebooks")

SQL_DIR = os.path.join(BASE_DIR, "sql")

SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")

DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")

DOCUMENTATION_DIR = os.path.join(BASE_DIR, "documentation")

# ============================================================
# SOURCE DATASETS
# ============================================================

CUSTOMERS_FILE = os.path.join(
    SOURCE_DIR,
    "customers.csv"
)

INVENTORY_FILE = os.path.join(
    SOURCE_DIR,
    "inventory.csv"
)

ORDERS_FILE = os.path.join(
    SOURCE_DIR,
    "orders.csv"
)

ORDER_ITEMS_FILE = os.path.join(
    SOURCE_DIR,
    "order_items.csv"
)

# ============================================================
# DATASET NAMES
# ============================================================

CUSTOMERS = "customers"

INVENTORY = "inventory"

ORDERS = "orders"

ORDER_ITEMS = "order_items"

# ============================================================
# PROJECT INFORMATION
# ============================================================

PROJECT_NAME = "E-Commerce Data Engineering Pipeline"

PROJECT_VERSION = "1.0"

print("Project configuration loaded successfully!")
print("Project:", PROJECT_NAME)
print("Source directory:", SOURCE_DIR)