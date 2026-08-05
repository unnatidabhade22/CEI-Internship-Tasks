-- ==========================================================
-- Query 1: Customer Purchase Frequency
-- ==========================================================

SELECT
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) AS total_orders,

    CASE
        WHEN COUNT(o.order_id) = 1 THEN 'One-Time'
        WHEN COUNT(o.order_id) BETWEEN 2 AND 4 THEN 'Occasional'
        ELSE 'Loyal'
    END AS customer_type

FROM customers c

JOIN orders o
ON c.customer_id = o.customer_id

GROUP BY c.customer_id, c.customer_name

ORDER BY total_orders DESC;

-- ==========================================================
-- Query 2: Customer Spend Tier
-- ==========================================================

SELECT

    c.customer_name,

    ROUND(SUM(oi.total_price),2) AS total_spend,

    CASE

        WHEN SUM(oi.total_price) < 5000 THEN 'Low'

        WHEN SUM(oi.total_price) BETWEEN 5000 AND 15000 THEN 'Medium'

        ELSE 'High'

    END AS spend_tier

FROM customers c

JOIN orders o
ON c.customer_id = o.customer_id

JOIN order_items oi
ON o.order_id = oi.order_id

GROUP BY c.customer_name

ORDER BY total_spend DESC;

-- ==========================================================
-- Query 3: RFM-style Customer Analysis
-- ==========================================================

SELECT

    c.customer_name,

    COUNT(DISTINCT o.order_id) AS frequency,

    ROUND(SUM(oi.total_price),2) AS monetary,

    MAX(o.order_date) AS last_purchase

FROM customers c

JOIN orders o
ON c.customer_id = o.customer_id

JOIN order_items oi
ON o.order_id = oi.order_id

GROUP BY c.customer_name

ORDER BY monetary DESC;