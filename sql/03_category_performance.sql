-- Revenue, units and share of total for each product category.
-- Demonstrates: JOIN, aggregation, window SUM() OVER () for % of total.
SELECT
    p.category,
    SUM(oi.quantity)                           AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
    ROUND(100.0 * SUM(oi.quantity * oi.unit_price)
          / SUM(SUM(oi.quantity * oi.unit_price)) OVER (), 1) AS pct_of_revenue
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders   o ON o.order_id   = oi.order_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;
