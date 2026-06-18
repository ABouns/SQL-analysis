-- Average order value and revenue per customer country.
-- Demonstrates: JOIN chain, AVG of an aggregated per-order subquery.
SELECT
    c.country,
    COUNT(DISTINCT c.customer_id)              AS customers,
    COUNT(DISTINCT o.order_id)                 AS orders,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
    ROUND(SUM(oi.quantity * oi.unit_price)
          / COUNT(DISTINCT o.order_id), 2)     AS avg_order_value
FROM customers c
JOIN orders o       ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id   = o.order_id
WHERE o.status = 'completed'
GROUP BY c.country
ORDER BY revenue DESC;
