-- Каркас запроса. Заполните CTE, не соединяя две детализации напрямую.
WITH service_cost AS (
  SELECT oi.order_id, /* выражение */ AS amount
  FROM order_items oi JOIN services s ON s.service_id = oi.service_id
  GROUP BY oi.order_id
), material_cost AS (
  SELECT oi.order_id, /* выражение */ AS amount
  FROM order_items oi
  JOIN material_norms mn ON mn.service_id = oi.service_id
  JOIN materials m ON m.material_id = mn.material_id
  GROUP BY oi.order_id
)
SELECT o.order_id, /* service, material, total */
FROM orders o
LEFT JOIN service_cost sc ON sc.order_id = o.order_id
LEFT JOIN material_cost mc ON mc.order_id = o.order_id
WHERE o.order_id = :order_id;
