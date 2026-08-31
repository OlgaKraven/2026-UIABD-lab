SELECT COUNT(*) AS tables_count FROM information_schema.tables WHERE table_schema='service_ops_recovery';
SELECT COUNT(*) AS branches_count FROM service_ops_recovery.branches;
SELECT COUNT(*) AS orders_count, ROUND(SUM(total),2) AS total_sum FROM service_ops_recovery.incident_orders;
SELECT branch_id, COUNT(*) AS order_count FROM service_ops_recovery.incident_orders GROUP BY branch_id ORDER BY branch_id;
CHECK TABLE service_ops_recovery.branches, service_ops_recovery.incident_orders;
