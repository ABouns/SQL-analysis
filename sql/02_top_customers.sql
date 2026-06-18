-- Top 10 customers by lifetime spend, with their rank and order count.
-- Demonstrates: CTE, multi-table JOIN, GROUP BY, window RANK().
WITH customer_spend AS (
    SELECT
        c.customer_id,
        c.name,
        c.country,
        COUNT(DISTINCT o.order_id)               AS orders,
        ROUND(SUM(oi.quantity * oi.unit_price),2) AS lifetime_value
    FROM customers c
    JOIN orders o       ON o.customer_id = c.customer_id
    JOIN order_items oi ON oi.order_id   = o.order_id
    WHERE o.status = 'completed'
    GROUP BY c.customer_id, c.name, c.country
)
SELECT
    RANK() OVER (ORDER BY lifetime_value DESC) AS rank,
    name, country, orders, lifetime_value
FROM customer_spend
ORDER BY lifetime_value DESC
LIMIT 10;
