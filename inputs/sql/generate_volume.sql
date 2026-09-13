-- MySQL 8.4. Только учебная база; @volume_rows задайте по варианту.
SET @volume_rows = COALESCE(@volume_rows, 25000);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status)
WITH digits AS (SELECT 0 n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9),
seq AS (SELECT 1+a.n+10*b.n+100*c.n+1000*d.n+10000*e.n n FROM digits a CROSS JOIN digits b CROSS JOIN digits c CROSS JOIN digits d CROSS JOIN digits e)
SELECT 100000+n, CONCAT('LOAD-',LPAD(n,6,'0')),1+MOD(n,3),1+MOD(n,9),DATE_ADD('2025-01-01',INTERVAL MOD(n,730) DAY),ELT(1+MOD(n,4),'NEW','IN_PROGRESS','DONE','CANCELLED')
FROM seq WHERE n<=@volume_rows AND NOT EXISTS(SELECT 1 FROM orders o WHERE o.order_id=100000+n);
INSERT INTO order_items(order_id,line_no,service_id,quantity)
SELECT order_id,1,1+MOD(order_id,4),1+MOD(order_id,3) FROM orders o
WHERE order_id>=100001 AND order_id<=100000+@volume_rows AND NOT EXISTS(SELECT 1 FROM order_items i WHERE i.order_id=o.order_id AND i.line_no=1);
