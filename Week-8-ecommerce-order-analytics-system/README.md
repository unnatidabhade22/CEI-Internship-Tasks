# Week 8 – E-Commerce Order Analytics System

## Objective

Design and develop an end-to-end E-Commerce Order Analytics System using Python, Pandas, SQLite, and SQL. The project covers dataset generation, data cleaning, database creation, SQL analytics, customer segmentation, and report generation through a Command-Line Interface (CLI).

---

## Features

- Generate realistic e-commerce datasets using Python.
- Introduce intentional data inconsistencies for cleaning practice.
- Clean and validate datasets using Pandas.
- Load cleaned data into an SQLite database.
- Perform SQL analytics using JOINs and Aggregations.
- Implement Window Functions and Common Table Expressions (CTEs).
- Perform Cohort and Retention Analysis.
- Segment customers using purchase frequency and spending patterns.
- Generate reports using a Python-based Command-Line Interface (CLI).
- Handle invalid inputs and database connection errors gracefully.

---

## Technologies Used

- Python
- Pandas
- SQLite
- SQL
- Faker
- Tabulate
- VS Code

---

## Dataset

The project uses four e-commerce datasets:

- customers.csv
- products.csv
- orders.csv
- order_items.csv

The datasets were generated using Python and include intentional inconsistencies for data cleaning and validation.

---

## Project Structure

```text
Week-8-ecommerce-order-analytics-system/
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── products.csv
│   │   ├── orders.csv
│   │   └── order_items.csv
│   │
│   └── cleaned/
│       ├── customers_clean.csv
│       ├── products_clean.csv
│       ├── orders_clean.csv
│       └── order_items_clean.csv
│
├── scripts/
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── load_to_sql.py
│   ├── run_queries.py
│   └── report_cli.py
│
├── sql/
│   ├── schema.sql
│   ├── aggregations.sql
│   ├── window_functions.sql
│   ├── cohort_analysis.sql
│   └── customer_segmentation.sql
│
├── ecommerce.db
├── Report.pdf
└── README.md
```

---

## Analytics Performed

- Revenue Analysis
- Product Performance Analysis
- Monthly Revenue Analysis
- Customer Lifetime Value Ranking
- Running Totals
- Moving Average Analysis
- Cohort Analysis
- Customer Retention Analysis
- Customer Segmentation
- RFM-style Analysis

---

## Command-Line Reports

The CLI tool supports the following reports:

- Revenue Report
- Top Products Report
- Customer Retention Report

It also validates user input and handles database connection errors.

---

## Report

The complete implementation details, screenshots, SQL query outputs, and project explanation are available in the **Report.pdf** file included in this repository.

---

## Outcome

Successfully developed a complete E-Commerce Order Analytics System by integrating Python, Pandas, SQLite, and SQL. The project demonstrates practical skills in data generation, data cleaning, SQL analytics, customer segmentation, cohort analysis, CLI-based reporting, and error handling while following a structured data analytics workflow.