-- Cumulative (running) revenue over time.
-- Demonstrates: CTE feeding a window SUM() OVER (ORDER BY ...).
WITH monthly AS (
    SELECT strftime('%Y-%m', o.order_date) AS month,
           SUM(oi.quantity * oi.unit_price) AS revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY month
)
SELECT
    month,
    ROUND(revenue, 2)                                          AS revenue,
    ROUND(SUM(revenue) OVER (ORDER BY month), 2)               AS cumulative_revenue
FROM monthly
ORDER BY month;
