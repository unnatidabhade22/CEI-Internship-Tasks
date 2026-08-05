-- ==========================================================
-- Query 1: Customer Cohort (First Purchase Month)
-- ==========================================================

WITH customer_cohort AS
(
    SELECT
        customer_id,
        MIN(strftime('%Y-%m', order_date)) AS cohort_month
    FROM orders
    GROUP BY customer_id
)

SELECT
    cohort_month,
    COUNT(customer_id) AS total_customers
FROM customer_cohort
GROUP BY cohort_month
ORDER BY cohort_month;

-- ==========================================================
-- Query 2: Monthly Active Customers
-- ==========================================================

SELECT
    strftime('%Y-%m', order_date) AS order_month,
    COUNT(DISTINCT customer_id) AS active_customers
FROM orders
GROUP BY order_month
ORDER BY order_month;

-- ==========================================================
-- Query 3: Repeat Customers
-- ==========================================================

SELECT
    customer_id,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(order_id) > 1
ORDER BY total_orders DESC;

-- ==========================================================
-- Query 4: One-Time Customers
-- ==========================================================

SELECT
    customer_id,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(order_id) = 1;

-- ==========================================================
-- Query 5: Monthly Retention Summary
-- ==========================================================

WITH customer_activity AS
(
    SELECT
        customer_id,
        strftime('%Y-%m', order_date) AS order_month
    FROM orders
)

SELECT
    order_month,
    COUNT(DISTINCT customer_id) AS retained_customers
FROM customer_activity
GROUP BY order_month
ORDER BY order_month;