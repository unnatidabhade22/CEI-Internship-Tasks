# SQL Advanced Analytics using MySQL

## Week 3 Internship Assignment

This project was completed as part of my Week 3 internship assignment.
The objective of this assignment was to learn and apply advanced SQL concepts like Subqueries, CTEs, Window Functions, JOINs, and customer sales analysis using the Superstore dataset.

In this assignment, I used MySQL Workbench to import the dataset, create separate tables, and perform advanced SQL queries for business analysis.

---

# Dataset Used

Dataset: Superstore Sales Dataset

The dataset contains information related to:

* Orders
* Customers
* Products
* Sales
* Profit
* Quantity
* Categories
* Regions

---

# Tools and Technologies Used

* MySQL Workbench 8.0 CE
* SQL
* GitHub

---

# Tasks Performed

## 1. Data Setup

* Imported the Superstore dataset into MySQL
* Renamed the imported table as `superstore_raw`
* Created separate tables:

  * customers
  * orders
  * products
* Inserted data using `SELECT DISTINCT`

---

## 2. Subquery Operations

Performed subquery-based analysis such as:

* Finding orders with sales greater than average sales
* Finding highest sales order for each customer

---

## 3. CTE (Common Table Expression) Operations

Used CTEs to:

* Calculate total sales for each customer
* Find customers whose sales are above average
* Simplify customer-level aggregation queries

---

## 4. Window Function Operations

Used Window Functions like:

* `ROW_NUMBER()`
* `RANK()`
* `DENSE_RANK()`

for:

* Customer ranking
* Order analysis
* Sales-based ranking

---

## 5. Final Combined Query

Created a final query using:

* JOIN
* CTE
* Window Function

to display:

* Customer Name
* Total Sales
* Customer Rank

---

# Mini Project – Customer Sales Insights

Performed business analysis using SQL queries to answer:

* Top 5 customers based on sales
* Bottom 5 customers based on sales
* Customers who made only one order
* Customers with above-average sales
* Highest order value per customer

---

# SQL Concepts Used

* SELECT
* WHERE
* GROUP BY
* ORDER BY
* LIMIT
* HAVING
* Subqueries
* CTEs
* JOINs
* Window Functions
* ROW_NUMBER()
* RANK()
* DENSE_RANK()

---

# Files Included

```text id="m4x8qp"
CEI-Internship-Tasks
│
└── Week-3-SQL-Advanced-Analytics
    │
    ├── Sample - Superstore.csv
    │
    ├── advanced_sql_queries.sql
    │
    ├── Query_Results.pdf
    │
    ├── Mini_Project_Results.pdf
    │
    └── README.md
```

---

# Key Learnings

Through this assignment, I learned:

* How to use advanced SQL concepts in real-world datasets
* How Subqueries and CTEs improve query readability
* How Window Functions are used for ranking and analysis
* How SQL is used for customer sales analysis
* How to organize SQL projects professionally

---

# Conclusion

This assignment helped me improve my understanding of advanced SQL analytics and business reporting techniques. It also gave me practical experience in writing optimized SQL queries and analyzing sales data using MySQL.

