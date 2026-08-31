-- MySQL 8.4: генерирует 25 000 синтетических заказов и позиций.
WITH RECURSIVE seq AS (
  SELECT 1 AS n
  UNION ALL SELECT n + 1 FROM seq WHERE n < 25000
)
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status)
SELECT 100000+n, CONCAT('LOAD-',LPAD(n,6,'0')), 1+MOD(n,3), 1+MOD(n,9),
       DATE_ADD('2025-01-01', INTERVAL MOD(n,730) DAY),
       ELT(1+MOD(n,4),'NEW','IN_PROGRESS','DONE','CANCELLED')
FROM seq;
INSERT INTO order_items(order_id,line_no,service_id,quantity)
SELECT order_id,1,1+MOD(order_id,4),1+MOD(order_id,3)
FROM orders WHERE order_id >= 100001;
