-- What share of customers placed more than one completed order?
-- Demonstrates: CTE, conditional aggregation, ratio in a single pass.
WITH per_customer AS (
    SELECT customer_id, COUNT(*) AS n_orders
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT
    COUNT(*)                                              AS active_customers,
    SUM(CASE WHEN n_orders > 1 THEN 1 ELSE 0 END)         AS repeat_customers,
    ROUND(100.0 * SUM(CASE WHEN n_orders > 1 THEN 1 ELSE 0 END)
          / COUNT(*), 1)                                  AS repeat_rate_pct
FROM per_customer;
