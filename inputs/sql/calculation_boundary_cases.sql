-- Выполняйте только в отдельной учебной базе или транзакции.
START TRANSACTION;
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES
(9001,'BOUNDARY-ZERO',1,1,'2026-07-01','NEW'),
(9002,'BOUNDARY-NEGATIVE',1,1,'2026-07-01','NEW'),
(9003,'BOUNDARY-NO-NORM',1,1,'2026-07-01','NEW');
-- Следующие две вставки должны быть отклонены CHECK-ограничением корректной схемы.
INSERT INTO order_items VALUES (9001,1,1,0);
INSERT INTO order_items VALUES (9002,1,1,-1);
INSERT INTO order_items VALUES (9003,1,1,1);
-- После фиксации доказательств отмените изменения.
ROLLBACK;
