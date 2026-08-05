import sqlite3
import argparse
import pandas as pd
from tabulate import tabulate
import os

# -------------------------------------
# Project Paths
# -------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "ecommerce.db")

# -------------------------------------
# Available Reports
# -------------------------------------

REPORTS = {

    "revenue": """
        SELECT
            c.customer_name,
            ROUND(SUM(oi.total_price),2) AS total_revenue
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY c.customer_name
        ORDER BY total_revenue DESC;
    """,

    "top_products": """
        SELECT
            p.product_name,
            SUM(oi.quantity) AS total_quantity
        FROM products p
        JOIN order_items oi
            ON p.product_id = oi.product_id
        GROUP BY p.product_name
        ORDER BY total_quantity DESC
        LIMIT 10;
    """,

    "retention": """
        SELECT
            strftime('%Y-%m', order_date) AS month,
            COUNT(DISTINCT customer_id) AS active_customers
        FROM orders
        GROUP BY month
        ORDER BY month;
    """
}

# -------------------------------------
# CLI Arguments
# -------------------------------------

parser = argparse.ArgumentParser(
    description="E-Commerce Analytics Reporting Tool"
)

parser.add_argument(
    "--report",
    required=True,
    help="Available reports: revenue, top_products, retention"
)

args = parser.parse_args()

# -------------------------------------
# Validate User Input
# -------------------------------------

if args.report not in REPORTS:

    print("\n Invalid report name!\n")

    print("Available Reports:")

    for report in REPORTS.keys():
        print(f" - {report}")

    exit()

# -------------------------------------
# Database Connection
# -------------------------------------

try:

    conn = sqlite3.connect(DB_PATH)

except Exception as e:

    print("Database connection failed!")

    print(e)

    exit()

# -------------------------------------
# Execute Query
# -------------------------------------

try:

    df = pd.read_sql_query(REPORTS[args.report], conn)

    if df.empty:

        print("\nNo records found.")

    else:

        print("\n")
        print("=" * 70)
        print(args.report.upper())
        print("=" * 70)

        print(
            tabulate(
                df,
                headers="keys",
                tablefmt="grid",
                showindex=False
            )
        )

except Exception as e:

    print("\nError while executing query.")

    print(e)

finally:

    conn.close()