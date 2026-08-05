import sqlite3
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db_path = os.path.join(BASE_DIR, "ecommerce.db")

sql_path = os.path.join(BASE_DIR, "sql", "customer_segmentation.sql")
conn = sqlite3.connect(db_path)

with open(sql_path, "r") as file:
    queries = file.read().split(";")

query_number = 1

for query in queries:

    query = query.strip()

    if query:

        print("\n" + "=" * 70)
        print(f"Query {query_number}")
        print("=" * 70)

        try:

            df = pd.read_sql_query(query, conn)

            print(df.head(10))

        except Exception as e:

            print(e)

        query_number += 1

conn.close()