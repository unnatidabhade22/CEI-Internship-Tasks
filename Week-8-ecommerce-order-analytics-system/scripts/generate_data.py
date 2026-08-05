import pandas as pd
import random
import os
from faker import Faker
from datetime import timedelta

# ---------------------------------------
# Initialize Faker
# ---------------------------------------

fake = Faker()

random.seed(42)
Faker.seed(42)

# ---------------------------------------
# Project Paths
# ---------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(RAW_DATA_PATH, exist_ok=True)

# ==========================================================
# Generate Customers Dataset
# ==========================================================

customers = []

for customer_id in range(1, 101):

    customers.append({
        "customer_id": customer_id,
        "customer_name": fake.name(),
        "email": fake.email(),
        "city": fake.city(),
        "state": fake.state(),
        "join_date": fake.date_between(start_date="-3y", end_date="today")
    })

customers_df = pd.DataFrame(customers)

customers_df.loc[5, "email"] = None
customers_df = pd.concat([customers_df, customers_df.iloc[[10]]], ignore_index=True)
customers_df.loc[15, "join_date"] = "2035-01-01"

customers_df.to_csv(
    os.path.join(RAW_DATA_PATH, "customers.csv"),
    index=False
)

print("customers.csv created successfully!")
print("Customers Shape:", customers_df.shape)

# ==========================================================
# Generate Products Dataset
# ==========================================================

categories = [
    "Electronics",
    "Clothing",
    "Home",
    "Sports",
    "Books"
]

products = []

for product_id in range(1, 51):

    products.append({

        "product_id": product_id,

        "product_name": fake.word().title() + " Product",

        "category": random.choice(categories),

        "price": round(random.uniform(100, 5000), 2),

        "stock": random.randint(5, 500)

    })

products_df = pd.DataFrame(products)

products_df.loc[4, "price"] = None
products_df.loc[8, "stock"] = -20
products_df = pd.concat([products_df, products_df.iloc[[12]]], ignore_index=True)

products_df.to_csv(
    os.path.join(RAW_DATA_PATH, "products.csv"),
    index=False
)

print("products.csv created successfully!")
print("Products Shape:", products_df.shape)

# ==========================================================
# Generate Orders Dataset
# ==========================================================

orders = []

for order_id in range(1, 201):

    order_date = fake.date_between(start_date="-2y", end_date="today")

    orders.append({

        "order_id": order_id,

        "customer_id": random.randint(1, 100),

        "order_date": order_date,

        "status": random.choice([
            "Completed",
            "Pending",
            "Cancelled"
        ])

    })

orders_df = pd.DataFrame(orders)

# Introduce inconsistencies

orders_df.loc[6, "customer_id"] = 999

orders_df.loc[12, "order_date"] = "2036-05-01"

orders_df = pd.concat(
    [orders_df, orders_df.iloc[[20]]],
    ignore_index=True
)

orders_df.to_csv(
    os.path.join(RAW_DATA_PATH, "orders.csv"),
    index=False
)

print("orders.csv created successfully!")
print("Orders Shape:", orders_df.shape)

# ==========================================================
# Generate Order Items Dataset
# ==========================================================

order_items = []

item_id = 1

for order in orders_df["order_id"].unique():

    num_items = random.randint(1, 4)

    for _ in range(num_items):

        quantity = random.randint(1, 5)

        price = round(random.uniform(100, 5000), 2)

        order_items.append({

            "item_id": item_id,

            "order_id": order,

            "product_id": random.randint(1, 50),

            "quantity": quantity,

            "unit_price": price,

            "total_price": round(quantity * price, 2)

        })

        item_id += 1

order_items_df = pd.DataFrame(order_items)

# Introduce inconsistencies

order_items_df.loc[3, "product_id"] = 888

order_items_df.loc[10, "quantity"] = None

order_items_df = pd.concat(
    [order_items_df, order_items_df.iloc[[15]]],
    ignore_index=True
)

order_items_df.to_csv(
    os.path.join(RAW_DATA_PATH, "order_items.csv"),
    index=False
)

print("order_items.csv created successfully!")
print("Order Items Shape:", order_items_df.shape)

print("\nAll raw datasets generated successfully!")