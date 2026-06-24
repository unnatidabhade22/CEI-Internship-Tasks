-- Week 2 SQL Assignment
-- SQL Data Analysis using MySQL

-- Section A : Basic Queries

CREATE DATABASE sql_assignment;

USE sql_assignment;

SHOW TABLES;

SELECT * FROM `sample - superstore` LIMIT 5;

RENAME TABLE `sample - superstore` TO sales_data;

SELECT * FROM sales_data LIMIT 10;

DESCRIBE sales_data;

SELECT COUNT(*) AS total_rows
FROM sales_data;

-- Section B : Filtering Queries

-- Checking missing sales values
SELECT *
FROM sales_data
WHERE Sales IS NULL;

-- Filter data for West region
SELECT *
FROM sales_data
WHERE Region = 'West';

-- Filter furniture category products
SELECT *
FROM sales_data
WHERE Category = 'Furniture';

-- Products with sales greater than 1000
SELECT *
FROM sales_data
WHERE Sales > 1000;

-- Multiple condition using AND
SELECT *
FROM sales_data
WHERE Region = 'West'
AND Sales > 1000;

-- Multiple condition using OR
SELECT *
FROM sales_data
WHERE Category = 'Furniture'
OR Category = 'Technology';

-- Section C : Aggregation Queries

-- Total sales by category
SELECT Category,
SUM(Sales) AS total_sales
FROM sales_data
GROUP BY Category;

-- Average sales by category
SELECT Category,
AVG(Sales) AS average_sales
FROM sales_data
GROUP BY Category;

-- Total quantity sold by category
SELECT Category,
SUM(Quantity) AS total_quantity
FROM sales_data
GROUP BY Category;

-- Total orders by region
SELECT Region,
COUNT(*) AS total_orders
FROM sales_data
GROUP BY Region;

-- Highest sales in each category
SELECT Category,
MAX(Sales) AS highest_sale
FROM sales_data
GROUP BY Category;

-- Lowest sales in each category
SELECT Category,
MIN(Sales) AS lowest_sale
FROM sales_data
GROUP BY Category;

-- Section D : Business Queries

-- Top 10 highest sales
SELECT *
FROM sales_data
ORDER BY Sales DESC
LIMIT 10;

-- Top selling products
SELECT `Product Name`,
SUM(Sales) AS total_sales
FROM sales_data
GROUP BY `Product Name`
ORDER BY total_sales DESC
LIMIT 10;

-- Top customers by sales
SELECT `Customer Name`,
SUM(Sales) AS total_sales
FROM sales_data
GROUP BY `Customer Name`
ORDER BY total_sales DESC
LIMIT 10;

-- Sales by category
SELECT Category,
SUM(Sales) AS total_sales
FROM sales_data
GROUP BY Category
ORDER BY total_sales DESC;

-- Lowest selling products
SELECT `Product Name`,
SUM(Sales) AS total_sales
FROM sales_data
GROUP BY `Product Name`
ORDER BY total_sales ASC
LIMIT 10;

-- Monthly sales trend
SELECT MONTH(`Order Date`) AS month,
SUM(Sales) AS total_sales
FROM sales_data
GROUP BY MONTH(`Order Date`)
ORDER BY month;

-- Section E : Validation Queries

-- Finding duplicate order IDs
SELECT `Order ID`,
COUNT(*) AS duplicate_count
FROM sales_data
GROUP BY `Order ID`
HAVING COUNT(*) > 1;

-- Total number of records
SELECT COUNT(*) AS total_records
FROM sales_data;

-- Count missing sales values
SELECT COUNT(*) AS missing_sales
FROM sales_data
WHERE Sales IS NULL;

-- Display unique categories
SELECT DISTINCT Category
FROM sales_data;

-- Average sales by region
SELECT Region,
AVG(Sales) AS average_sales
FROM sales_data
GROUP BY Region
ORDER BY average_sales DESC;
