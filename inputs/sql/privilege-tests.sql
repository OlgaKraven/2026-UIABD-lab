-- Выполняйте каждый блок под указанной учебной учётной записью.
SELECT CURRENT_USER(), USER(), CURRENT_ROLE();
SELECT order_id, status FROM service_ops.orders ORDER BY order_id LIMIT 3;
INSERT INTO service_ops.stock_movements(material_id,branch_id,movement_type,quantity,reference_no)
VALUES (1,1,'RECEIPT',5,'PRIV-TEST-01');
UPDATE service_ops.orders SET status='IN_PROGRESS' WHERE order_id=1001;
DELETE FROM service_ops.stock_movements WHERE reference_no='PRIV-TEST-01';
DROP TABLE service_ops.orders;
