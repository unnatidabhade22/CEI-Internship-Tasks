-- ==========================================================
-- Query 1: Total Revenue per Customer
-- ==========================================================

SELECT
    c.customer_id,
    c.customer_name,
    ROUND(SUM(oi.total_price),2) AS total_revenue
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_revenue DESC;

-- ==========================================================
-- Query 2: Revenue per Product Category
-- ==========================================================

SELECT
    p.category,
    ROUND(SUM(oi.total_price),2) AS total_revenue
FROM products p
JOIN order_items oi
ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- ==========================================================
-- Query 3: Monthly Revenue
-- ==========================================================

SELECT
    strftime('%Y-%m',o.order_date) AS month,
    ROUND(SUM(oi.total_price),2) AS monthly_revenue
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;

-- ==========================================================
-- Query 4: Top Products by Quantity Sold
-- ==========================================================

SELECT
    p.product_name,
    SUM(oi.quantity) AS total_quantity
FROM products p
JOIN order_items oi
ON p.product_id = oi.product_id
GROUP BY p.product_name
ORDER BY total_quantity DESC
LIMIT 10;

-- ==========================================================
-- Query 5: Top Products by Revenue
-- ==========================================================

SELECT
    p.product_name,
    ROUND(SUM(oi.total_price),2) AS revenue
FROM products p
JOIN order_items oi
ON p.product_id = oi.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 10;

-- ==========================================================
-- Query 6: Average Order Value (AOV)
-- ==========================================================

SELECT
    ROUND(AVG(order_total),2) AS average_order_value
FROM
(
    SELECT
        order_id,
        SUM(total_price) AS order_total
    FROM order_items
    GROUP BY order_id
);

-- ==========================================================
-- Query 7: Customer Wise Average Order Value
-- ==========================================================

SELECT
    c.customer_name,
    ROUND(AVG(t.order_total),2) AS average_order_value
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id

JOIN
(
    SELECT
        order_id,
        SUM(total_price) AS order_total
    FROM order_items
    GROUP BY order_id
) t

ON o.order_id=t.order_id

GROUP BY c.customer_name
ORDER BY average_order_value DESC;