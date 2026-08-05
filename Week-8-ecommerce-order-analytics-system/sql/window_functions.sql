-- ==========================================================
-- Query 1: Rank Customers by Lifetime Value
-- ==========================================================

SELECT
    customer_name,
    total_revenue,
    RANK() OVER (ORDER BY total_revenue DESC) AS customer_rank
FROM
(
    SELECT
        c.customer_name,
        SUM(oi.total_price) AS total_revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY c.customer_name
);

-- ==========================================================
-- Query 2: Running Monthly Revenue
-- ==========================================================

WITH monthly_sales AS
(
    SELECT
        strftime('%Y-%m', o.order_date) AS month,
        SUM(oi.total_price) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY month
)

SELECT
    month,
    revenue,
    SUM(revenue) OVER
    (
        ORDER BY month
    ) AS running_total
FROM monthly_sales;

-- ==========================================================
-- Query 3: Moving Average Revenue
-- ==========================================================

WITH monthly_sales AS
(
    SELECT
        strftime('%Y-%m', o.order_date) AS month,
        SUM(oi.total_price) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY month
)

SELECT
    month,
    revenue,

    ROUND(
        AVG(revenue) OVER
        (
            ORDER BY month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_average

FROM monthly_sales;

-- ==========================================================
-- Query 4: Monthly Revenue using CTE
-- ==========================================================

WITH monthly_revenue AS
(
    SELECT

        strftime('%Y-%m', o.order_date) AS month,

        ROUND(SUM(oi.total_price),2) AS revenue

    FROM orders o

    JOIN order_items oi

    ON o.order_id = oi.order_id

    GROUP BY month
)

SELECT *

FROM monthly_revenue

ORDER BY month;

-- ==========================================================
-- Query 5: Monthly Growth
-- ==========================================================

WITH monthly_revenue AS
(
    SELECT

        strftime('%Y-%m', o.order_date) AS month,

        SUM(oi.total_price) AS revenue

    FROM orders o

    JOIN order_items oi

    ON o.order_id = oi.order_id

    GROUP BY month
)

SELECT

    month,

    revenue,

    revenue -

    LAG(revenue)

    OVER(ORDER BY month)

    AS growth

FROM monthly_revenue;