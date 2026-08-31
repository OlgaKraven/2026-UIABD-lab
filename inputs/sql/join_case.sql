-- В запросе намеренно допущена ошибка соединения. Найдите её по кардинальности.
SELECT o.order_id, o.order_date, c.customer_name, b.branch_name
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
JOIN branches AS b ON b.branch_id = o.customer_id
ORDER BY o.order_id;
