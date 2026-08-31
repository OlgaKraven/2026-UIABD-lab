-- Намеренно неэффективный учебный запрос. Не исправляйте до фиксации исходного плана.
SELECT o.order_id, o.order_date, b.branch_name, c.customer_name,
       SUM(oi.quantity * s.unit_price) AS service_amount
FROM orders o
JOIN branches b ON b.branch_id = o.branch_id
JOIN customers c ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN services s ON s.service_id = oi.service_id
WHERE YEAR(o.order_date) = 2026
  AND MONTH(o.order_date) BETWEEN 2 AND 6
  AND LOWER(b.branch_name) = LOWER('Центр')
GROUP BY o.order_id, o.order_date, b.branch_name, c.customer_name
ORDER BY o.order_date DESC, o.order_id;
