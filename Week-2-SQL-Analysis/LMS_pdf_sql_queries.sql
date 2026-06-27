-- Week 2 LMS SQL Assignment

CREATE DATABASE lms_sql_assignment;

USE lms_sql_assignment;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    state VARCHAR(50),
    join_date DATE
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    unit_price DECIMAL(10,2),
    stock_qty INT
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    status VARCHAR(30),
    total_amount DECIMAL(10,2),
    
    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    discount_pct DECIMAL(5,2),

    FOREIGN KEY (order_id)
    REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
    REFERENCES products(product_id)
);

SHOW TABLES;

INSERT INTO customers VALUES
(101, 'Rahul', 'Sharma', 'Maharashtra', '2024-01-15'),
(102, 'Priya', 'Verma', 'Delhi', '2023-11-10'),
(103, 'Aman', 'Patel', 'Gujarat', '2024-03-20'),
(104, 'Sneha', 'Joshi', 'Maharashtra', '2024-07-05'),
(105, 'Karan', 'Mehta', 'Rajasthan', '2023-09-18');

INSERT INTO products VALUES
(201, 'Laptop', 'Electronics', 55000.00, 20),
(202, 'Headphones', 'Electronics', 2500.00, 50),
(203, 'Office Chair', 'Furniture', 7000.00, 15),
(204, 'Notebook', 'Stationery', 100.00, 200),
(205, 'Smartphone', 'Electronics', 30000.00, 25);

INSERT INTO orders VALUES
(1001, 101, '2024-08-10', 'Delivered', 57500.00),
(1002, 102, '2024-08-12', 'Pending', 2500.00),
(1003, 103, '2024-08-15', 'Cancelled', 7000.00),
(1004, 104, '2024-08-20', 'Delivered', 30100.00),
(1005, 101, '2024-08-25', 'Delivered', 100.00);

INSERT INTO order_items VALUES
(1, 1001, 201, 1, 55000.00, 5.00),
(2, 1001, 202, 1, 2500.00, 0.00),
(3, 1002, 202, 1, 2500.00, 10.00),
(4, 1003, 203, 1, 7000.00, 0.00),
(5, 1004, 205, 1, 30000.00, 2.00),
(6, 1004, 204, 1, 100.00, 0.00),
(7, 1005, 204, 1, 100.00, 0.00);

-- Section A : Basic Queries

-- Q1. Display all customers
SELECT * FROM customers;

-- Q2. Display all products
SELECT * FROM products;

-- Q3. Display all orders
SELECT * FROM orders;

-- Q4. Display all order items
SELECT * FROM order_items;

-- Q5. Count total customers
SELECT COUNT(*) AS total_customers
FROM customers;

-- Q6. Count total products
SELECT COUNT(*) AS total_products
FROM products;

-- Section B : Filtering Queries

-- Q7. Retrieve all orders with status = 'Delivered'
SELECT *
FROM orders
WHERE status = 'Delivered';

-- Q8. Find all products in Electronics category with unit_price greater than 2000
SELECT *
FROM products
WHERE category = 'Electronics'
AND unit_price > 2000;

-- Q9. List customers who joined in 2024 and belong to Maharashtra
SELECT *
FROM customers
WHERE YEAR(join_date) = 2024
AND state = 'Maharashtra';

-- Q10. Find orders placed between given dates and not cancelled
SELECT *
FROM orders
WHERE order_date BETWEEN '2024-08-10' AND '2024-08-25'
AND status != 'Cancelled';

-- Q11. Sample query using order_date index
SELECT *
FROM orders
WHERE order_date = '2024-08-10';

-- Q12. Index friendly query for join_date
SELECT *
FROM customers
WHERE join_date BETWEEN '2024-01-01' AND '2024-12-31';

-- Section C : Aggregation Queries

-- Q13. Count total number of orders
SELECT COUNT(*) AS total_orders
FROM orders;

-- Q14. Find total revenue from delivered orders
SELECT SUM(total_amount) AS total_revenue
FROM orders
WHERE status = 'Delivered';

-- Q15. Calculate average unit_price in each category
SELECT category,
AVG(unit_price) AS average_price
FROM products
GROUP BY category;

-- Q16. Count orders and total revenue by order status
SELECT status,
COUNT(*) AS order_count,
SUM(total_amount) AS total_revenue
FROM orders
GROUP BY status
ORDER BY total_revenue DESC;

-- Q17. Find maximum and minimum product price in each category
SELECT category,
MAX(unit_price) AS max_price,
MIN(unit_price) AS min_price
FROM products
GROUP BY category;

-- Q18. Categories where average unit_price is greater than 2000
SELECT category,
AVG(unit_price) AS average_price
FROM products
GROUP BY category
HAVING AVG(unit_price) > 2000;

-- Section D : Joins

-- Q19. INNER JOIN between orders and customers
SELECT o.order_id,
o.order_date,
c.first_name,
c.last_name,
o.total_amount
FROM orders o
INNER JOIN customers c
ON o.customer_id = c.customer_id;

-- Q20. LEFT JOIN to display all customers and their orders
SELECT c.customer_id,
c.first_name,
c.last_name,
o.order_id,
o.order_date
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;

-- Q21. JOIN query using orders, order_items and products tables
SELECT oi.order_id,
p.product_name,
oi.quantity,
oi.unit_price,
oi.discount_pct
FROM order_items oi
INNER JOIN products p
ON oi.product_id = p.product_id;

-- Q22. Example of RIGHT JOIN
SELECT o.order_id,
c.first_name
FROM orders o
RIGHT JOIN customers c
ON o.customer_id = c.customer_id;

-- Q23. Display orders table
SELECT *
FROM orders;

-- Section E : Advanced Queries

-- Q24. Classify products into price tiers using CASE
SELECT product_name,
unit_price,
CASE
WHEN unit_price < 1000 THEN 'Budget'
WHEN unit_price BETWEEN 1000 AND 3000 THEN 'Mid-Range'
ELSE 'Premium'
END AS price_tier
FROM products;

-- Q25. Count delivered and not delivered orders
SELECT
SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders,
SUM(CASE WHEN status != 'Delivered' THEN 1 ELSE 0 END) AS not_delivered_orders
FROM orders;

-- Q26. ACID Properties
-- A = Atomicity
-- C = Consistency
-- I = Isolation
-- D = Durability

-- Q27. SQL Transaction Example

START TRANSACTION;

INSERT INTO orders
VALUES (1011, 102, CURDATE(), 'Pending', 1598.00);

INSERT INTO order_items
VALUES
(8, 1011, 202, 1, 2500.00, 5.00),
(9, 1011, 204, 2, 100.00, 0.00);

UPDATE products
SET stock_qty = stock_qty - 1
WHERE product_id = 202;

UPDATE products
SET stock_qty = stock_qty - 2
WHERE product_id = 204;

COMMIT;
