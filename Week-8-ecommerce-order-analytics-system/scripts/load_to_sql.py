import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db_path = os.path.join(BASE_DIR, "ecommerce.db")

clean_path = os.path.join(BASE_DIR, "data", "cleaned")

conn = sqlite3.connect(db_path)

customers = pd.read_csv(os.path.join(clean_path, "customers_clean.csv"))
products = pd.read_csv(os.path.join(clean_path, "products_clean.csv"))
orders = pd.read_csv(os.path.join(clean_path, "orders_clean.csv"))
order_items = pd.read_csv(os.path.join(clean_path, "order_items_clean.csv"))

customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)
order_items.to_sql("order_items", conn, if_exists="replace", index=False)

print("All tables loaded successfully into SQLite!")

print("\nRow Counts")

print("Customers :", len(customers))
print("Products :", len(products))
print("Orders :", len(orders))
print("Order Items :", len(order_items))

conn.close()