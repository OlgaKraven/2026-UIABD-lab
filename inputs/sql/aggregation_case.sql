-- Детализация для самостоятельного построения агрегата.
SELECT o.order_id, o.branch_id, o.status, o.order_date,
       oi.quantity, s.unit_price, oi.quantity * s.unit_price AS service_amount
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN services s ON s.service_id = oi.service_id
WHERE o.order_date >= :date_from AND o.order_date < :date_to_exclusive;
