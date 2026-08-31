-- После создания триггера выполняйте по одному UPDATE и проверяйте аудит.
SELECT COUNT(*) AS audit_before FROM order_status_audit WHERE order_id=1001;
UPDATE orders SET status=status WHERE order_id=1001;
UPDATE orders SET status='IN_PROGRESS' WHERE order_id=1001;
SELECT * FROM order_status_audit WHERE order_id=1001 ORDER BY audit_id;
