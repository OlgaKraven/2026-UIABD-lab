INSERT INTO branches VALUES (1,'Центр','Москва'),(2,'Север','Химки'),(3,'Юг','Подольск');
INSERT INTO customers VALUES
(1,'ООО Альфа','alpha@example.test'),(2,'АО Вектор','vector@example.test'),(3,'ИП Волков','volkov@example.test'),
(4,'ООО Гамма','gamma@example.test'),(5,'АО Дельта','delta@example.test'),(6,'ООО Маяк','mayak@example.test'),
(7,'ООО Парус','parus@example.test'),(8,'ИП Орлова','orlova@example.test'),(9,'АО Ритм','ritm@example.test');
INSERT INTO services VALUES (1,'Диагностика',2500.00),(2,'Регламентное обслуживание',7200.00),(3,'Аварийный выезд',12500.00),(4,'Монтаж оборудования',18000.00);
INSERT INTO materials VALUES (1,'Кабель','м',95.00),(2,'Разъём','шт',180.00),(3,'Фильтр','шт',850.00),(4,'Крепёж','компл',320.00);
INSERT INTO material_norms VALUES (2,3,1.000),(3,1,12.000),(3,2,4.000),(4,1,25.000),(4,2,8.000),(4,4,2.000);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES
(1001,'SO-1001',1,1,'2026-02-03','NEW'),(1002,'SO-1002',1,2,'2026-02-14','IN_PROGRESS'),
(1003,'SO-1003',1,3,'2026-02-28','DONE'),(1004,'SO-1004',2,4,'2026-03-04','DONE'),
(1005,'SO-1005',2,5,'2026-03-18','CANCELLED'),(1006,'SO-1006',2,6,'2026-03-31','IN_PROGRESS'),
(1007,'SO-1007',3,7,'2026-04-02','NEW'),(1008,'SO-1008',3,8,'2026-04-19','DONE'),
(1009,'SO-1009',3,9,'2026-04-30','DONE'),(1010,'SO-1010',1,4,'2026-05-11','IN_PROGRESS'),
(1011,'SO-1011',2,5,'2026-05-25','DONE'),(1012,'SO-1012',3,6,'2026-06-06','NEW');
INSERT INTO order_items VALUES
(1001,1,1,1),(1001,2,3,1),(1002,1,2,2),(1003,1,4,1),(1004,1,1,1),
(1005,1,2,1),(1006,1,3,2),(1007,1,1,3),(1008,1,4,1),(1008,2,2,1),
(1009,1,3,1),(1010,1,4,2),(1010,2,1,1),(1011,1,2,4),(1012,1,3,1);
INSERT INTO material_balances VALUES (1,1,500),(2,1,200),(3,1,80),(4,1,100),(1,2,250),(2,2,100),(3,2,60),(4,2,70),(1,3,300),(2,3,130),(3,3,75),(4,3,90);

-- Extended assessed orders 1013..1030; original records retained.
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1013,'SO-1013',1,4,'2026-04-15','DONE');
INSERT INTO order_items VALUES(1013,1,1,2);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1014,'SO-1014',2,5,'2026-05-15','DONE');
INSERT INTO order_items VALUES(1014,1,2,3);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1015,'SO-1015',3,6,'2026-06-15','DONE');
INSERT INTO order_items VALUES(1015,1,3,1);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1016,'SO-1016',1,7,'2026-02-15','DONE');
INSERT INTO order_items VALUES(1016,1,4,2);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1017,'SO-1017',2,8,'2026-03-15','DONE');
INSERT INTO order_items VALUES(1017,1,1,3);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1018,'SO-1018',3,9,'2026-04-15','DONE');
INSERT INTO order_items VALUES(1018,1,2,1);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1019,'SO-1019',1,1,'2026-05-15','DONE');
INSERT INTO order_items VALUES(1019,1,3,2);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1020,'SO-1020',2,2,'2026-06-15','DONE');
INSERT INTO order_items VALUES(1020,1,4,3);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1021,'SO-1021',3,3,'2026-02-15','DONE');
INSERT INTO order_items VALUES(1021,1,1,1);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1022,'SO-1022',1,4,'2026-03-15','DONE');
INSERT INTO order_items VALUES(1022,1,2,2);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1023,'SO-1023',2,5,'2026-04-15','DONE');
INSERT INTO order_items VALUES(1023,1,3,3);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1024,'SO-1024',3,6,'2026-05-15','DONE');
INSERT INTO order_items VALUES(1024,1,4,1);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1025,'SO-1025',1,7,'2026-06-15','DONE');
INSERT INTO order_items VALUES(1025,1,1,2);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1026,'SO-1026',2,8,'2026-02-15','DONE');
INSERT INTO order_items VALUES(1026,1,2,3);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1027,'SO-1027',3,9,'2026-03-15','DONE');
INSERT INTO order_items VALUES(1027,1,3,1);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1028,'SO-1028',1,1,'2026-04-15','DONE');
INSERT INTO order_items VALUES(1028,1,4,2);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1029,'SO-1029',2,2,'2026-05-15','DONE');
INSERT INTO order_items VALUES(1029,1,1,3);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES(1030,'SO-1030',3,3,'2026-06-15','DONE');
INSERT INTO order_items VALUES(1030,1,2,1);
