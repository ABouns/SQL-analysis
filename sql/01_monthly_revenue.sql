-- Monthly net revenue trend (completed orders only).
-- Demonstrates: JOIN, aggregation, date bucketing, filtering.
SELECT
    strftime('%Y-%m', o.order_date)          AS month,
    COUNT(DISTINCT o.order_id)               AS orders,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY month
ORDER BY month;
