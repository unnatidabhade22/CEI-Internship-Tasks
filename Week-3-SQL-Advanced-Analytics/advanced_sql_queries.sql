-- Week 3 SQL Advanced Analytics Assignment

-- Create database

CREATE DATABASE week3_sql_analysis;

USE week3_sql_analysis;

-- Rename imported table

RENAME TABLE `Sample - Superstore`
TO superstore_raw;

-- View sample data

SELECT *
FROM superstore_raw
LIMIT 10;

-- Output:
-- First 10 records from the dataset were displayed successfully.

-- Section 1 : Creating Tables

-- Q1. Create customers table from raw dataset

CREATE TABLE customers AS
SELECT DISTINCT
`Customer ID`,
`Customer Name`,
Segment,
Country,
City,
State,
Region
FROM superstore_raw;

-- View customers table

SELECT *
FROM customers
LIMIT 10;

-- Output:
-- Customers table created successfully with unique customer details.

-- Q2. Create orders table from raw dataset

CREATE TABLE orders AS
SELECT DISTINCT
`Order ID`,
`Order Date`,
`Ship Date`,
`Ship Mode`,
`Customer ID`,
Sales,
Quantity,
Discount,
Profit
FROM superstore_raw;

-- View orders table

SELECT *
FROM orders
LIMIT 10;

-- Output:
-- Orders table created successfully with order related information.

-- Q3. Create products table from raw dataset

CREATE TABLE products AS
SELECT DISTINCT
`Product ID`,
`Product Name`,
Category,
`Sub-Category`
FROM superstore_raw;

-- View products table

SELECT *
FROM products
LIMIT 10;

-- Output:
-- Products table created successfully with unique product records.

-- Section 2 : Subqueries

-- Q4. Find orders where sales are greater than average sales

SELECT *
FROM orders
WHERE Sales > (
SELECT AVG(Sales)
FROM orders
);

-- Output:
-- Orders with sales greater than average sales were displayed.

-- Q5. Find highest order value for each customer

SELECT
`Customer ID`,
MAX(Sales) AS highest_sales
FROM orders
GROUP BY `Customer ID`;

-- Output:
-- Highest sales value for each customer was displayed successfully.

-- Section 3 : CTE Queries

-- Q6. Calculate total sales for each customer using CTE

WITH customer_sales AS (
SELECT
`Customer ID`,
SUM(Sales) AS total_sales
FROM orders
GROUP BY `Customer ID`
)
SELECT *
FROM customer_sales;

-- Output:
-- Total sales for each customer were calculated successfully.

-- Q7. Find customers whose total sales are above average

WITH customer_sales AS (
SELECT
`Customer ID`,
SUM(Sales) AS total_sales
FROM orders
GROUP BY `Customer ID`
)

SELECT *
FROM customer_sales
WHERE total_sales > (
SELECT AVG(total_sales)
FROM customer_sales
);

-- Output:
-- Customers having above average total sales were displayed.

-- Section 4 : Window Functions

-- Q8. Rank customers based on total sales

WITH customer_sales AS (
SELECT
`Customer ID`,
SUM(Sales) AS total_sales
FROM orders
GROUP BY `Customer ID`
)
SELECT
`Customer ID`,
total_sales,
RANK() OVER (ORDER BY total_sales DESC) AS customer_rank
FROM customer_sales;

-- Output:
-- Customers ranked according to total sales successfully.

-- Q9. Assign row numbers to each order within a customer

SELECT
`Customer ID`,
`Order ID`,
Sales,
ROW_NUMBER() OVER (
PARTITION BY `Customer ID`
ORDER BY Sales DESC
) AS row_number_value
FROM orders;

-- Output:
-- Row numbers assigned to orders within each customer.

-- Q10. Apply dense rank on customer sales

WITH customer_sales AS (
SELECT
`Customer ID`,
SUM(Sales) AS total_sales
FROM orders
GROUP BY `Customer ID`
)

SELECT
`Customer ID`,
total_sales,
DENSE_RANK() OVER (ORDER BY total_sales DESC) AS dense_rank_value
FROM customer_sales;

-- Output:
-- Dense ranking applied on customer sales successfully.

-- Q11. Display top 3 customers based on total sales

WITH customer_sales AS (
SELECT
`Customer ID`,
SUM(Sales) AS total_sales
FROM orders
GROUP BY `Customer ID`
)
SELECT
`Customer ID`,
total_sales,
RANK() OVER (ORDER BY total_sales DESC) AS customer_rank
FROM customer_sales
LIMIT 3;

-- Output:
-- Top 3 customers based on sales were displayed.

-- Section 5 : Final Combined Query

-- Q12. Display customer name, total sales and rank

WITH customer_sales AS (
SELECT
`Customer ID`,
SUM(Sales) AS total_sales
FROM orders
GROUP BY `Customer ID`
)

SELECT
c.`Customer Name`,
cs.total_sales,
RANK() OVER (ORDER BY cs.total_sales DESC) AS customer_rank
FROM customer_sales cs
JOIN customers c
ON cs.`Customer ID` = c.`Customer ID`;

-- Output:
-- Customer name, total sales and rank displayed together successfully.

-- Section 6 : Business Problems

-- Q13. Find top 5 customers based on sales

WITH customer_sales AS (
SELECT
`Customer ID`,
SUM(Sales) AS total_sales
FROM orders
GROUP BY `Customer ID`
)

SELECT
c.`Customer Name`,
total_sales
FROM customer_sales cs
JOIN customers c
ON cs.`Customer ID` = c.`Customer ID`
ORDER BY total_sales DESC
LIMIT 5;

-- Output:
-- Top 5 customers based on total sales were displayed.

-- Q14. Find bottom 5 customers based on sales

WITH customer_sales AS (
SELECT
`Customer ID`,
SUM(Sales) AS total_sales
FROM orders
GROUP BY `Customer ID`
)

SELECT
c.`Customer Name`,
total_sales
FROM customer_sales cs
JOIN customers c
ON cs.`Customer ID` = c.`Customer ID`
ORDER BY total_sales ASC
LIMIT 5;

-- Output:
-- Bottom 5 customers based on total sales were displayed.

-- Q15. Find customers who made only one order

SELECT
`Customer ID`,
COUNT(`Order ID`) AS total_orders
FROM orders
GROUP BY `Customer ID`
HAVING COUNT(`Order ID`) = 1;

-- Output:
-- Customers who placed only one order were displayed.

-- Q16. Find customers with above average sales

WITH customer_sales AS (
SELECT
`Customer ID`,
SUM(Sales) AS total_sales
FROM orders
GROUP BY `Customer ID`
)

SELECT *
FROM customer_sales
WHERE total_sales > (
SELECT AVG(total_sales)
FROM customer_sales
);

-- Output:
-- Customers with above average sales were displayed successfully.

-- Q17. Find highest order value per customer

SELECT
`Customer ID`,
MAX(Sales) AS highest_order_value
FROM orders
GROUP BY `Customer ID`;

-- Output:
-- Highest order value for each customer displayed successfully.

-- Section 7 : Basic Validation Queries

-- Check total records in customers table

SELECT COUNT(*) AS total_customers
FROM customers;

-- Output:
-- Total number of customers displayed successfully.

-- Check total records in orders table

SELECT COUNT(*) AS total_orders
FROM orders;

-- Output:
-- Total number of orders displayed successfully.

-- Check total records in products table

SELECT COUNT(*) AS total_products
FROM products;

-- Output:
-- Total number of products displayed successfully.

-- View unique categories

SELECT DISTINCT Category
FROM products;

-- Output:
-- Unique product categories displayed successfully.
