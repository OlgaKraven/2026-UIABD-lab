from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def write(relative: str, text: str) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.strip() + "\n", encoding="utf-8")


def csv_document(header: list[str], rows: list[list[object]]) -> str:
    def encode(value: object) -> str:
        text = str(value)
        return f'"{text.replace(chr(34), chr(34) * 2)}"' if any(char in text for char in ',"\n') else text
    return "\n".join([",".join(header), *[",".join(encode(value) for value in row) for row in rows]])


def main() -> None:
    files: dict[str, str] = {
        "inputs/variants/c3-s6-variants.csv": """
variant,student_suffix,service_name,port,datadir,database_name,collation,reader_user,operator_user,allowed_host,incident_case,log_window
1,01,MySQL84_UIABD01,3311,C:/mysql-data/uiabd01,service_ops_01,utf8mb4_0900_ai_ci,reader01,operator01,localhost,C01,W01
2,02,MySQL84_UIABD02,3312,C:/mysql-data/uiabd02,service_ops_02,utf8mb4_0900_as_ci,reader02,operator02,localhost,C02,W02
3,03,MySQL84_UIABD03,3313,C:/mysql-data/uiabd03,service_ops_03,utf8mb4_unicode_ci,reader03,operator03,127.0.0.1,C03,W03
4,04,MySQL84_UIABD04,3314,C:/mysql-data/uiabd04,service_ops_04,utf8mb4_0900_ai_ci,reader04,operator04,127.0.0.1,C04,W04
5,05,MySQL84_UIABD05,3315,C:/mysql-data/uiabd05,service_ops_05,utf8mb4_0900_as_ci,reader05,operator05,localhost,C05,W05
6,06,MySQL84_UIABD06,3316,C:/mysql-data/uiabd06,service_ops_06,utf8mb4_unicode_ci,reader06,operator06,localhost,C06,W06
""",
        "inputs/variants/c4-s7-variants.csv": """
variant,branch_id,date_from,date_to,statuses,minimum_total,order_id,material_id,slow_branch,volume_rows
1,1,2026-02-01,2026-02-28,"NEW|IN_PROGRESS",15000,1001,1,1,25000
2,2,2026-02-01,2026-03-31,"DONE|CANCELLED",10000,1004,2,2,30000
3,3,2026-03-01,2026-04-30,"NEW|DONE",20000,1007,3,3,35000
4,1,2026-04-01,2026-05-31,"IN_PROGRESS|DONE",25000,1010,1,1,40000
5,2,2026-05-01,2026-06-30,"NEW|IN_PROGRESS|DONE",18000,1013,3,2,45000
6,3,2026-06-01,2026-07-31,"DONE",12000,1016,2,3,50000
""",
        "inputs/variants/c4-s8-variants.csv": """
variant,metric,warning_threshold,critical_threshold,evaluation_window,platform_priority,incident_id
1,connections_used_pct,65,80,5m,reliability,I01
2,p95_query_seconds,0.8,1.5,10m,compatibility,I02
3,disk_free_pct,25,15,15m,observability,I03
4,error_rate_per_min,3,8,5m,cost,I04
5,connections_used_pct,70,85,10m,portability,I05
6,p95_query_seconds,1.0,2.0,15m,skills_available,I06
""",
        "inputs/configuration/my.ini.template": """
[mysqld]
# Замените значения по карточке варианта. Не добавляйте пароль.
port=PORT_FROM_VARIANT
datadir=DATADIR_FROM_VARIANT
character-set-server=utf8mb4
collation-server=COLLATION_FROM_VARIANT
log_error=DATADIR_FROM_VARIANT/mysql-error.log

[client]
port=PORT_FROM_VARIANT
default-character-set=utf8mb4
""",
        "inputs/configuration/health-check-form.csv": """
check,expected,evidence_command,actual,status,comment
OS service,RUNNING,sc query <service>,,,
Listening port,variant port,Get-NetTCPConnection -State Listen,,, 
Server response,mysqld is alive,mysqladmin ping,,, 
SQL connection,one row returned,"SELECT CONNECTION_ID(), @@port, @@datadir;",,,
Configuration consistency,all values match,compare evidence,,, 
""",
        "inputs/configuration/schema-checklist.csv": """
object_type,object_name,parent,required_key
TABLE,branches,service_ops,PRIMARY KEY (branch_id)
TABLE,customers,service_ops,PRIMARY KEY (customer_id)
TABLE,services,service_ops,PRIMARY KEY (service_id)
TABLE,materials,service_ops,PRIMARY KEY (material_id)
TABLE,orders,service_ops,FK branch_id and customer_id
TABLE,order_items,service_ops,FK order_id and service_id
TABLE,material_norms,service_ops,FK service_id and material_id
TABLE,stock_movements,service_ops,FK material_id
TABLE,material_balances,service_ops,FK material_id and branch_id
TABLE,order_status_audit,service_ops,FK order_id
""",
        "inputs/configuration/import-rules.md": """
# Правила импорта заказов

- Файл — UTF-8, разделитель `;`, первая строка содержит заголовок.
- `external_order_no` обязателен и уникален в пределах импорта.
- `branch_id` должен существовать в `branches`.
- `customer_id` должен существовать в `customers`.
- `order_date` — календарная дата в формате `YYYY-MM-DD`, не позднее `2026-12-31`.
- `quantity` — целое число от 1 до 50.
- `status` — одно из `NEW`, `IN_PROGRESS`, `DONE`, `CANCELLED`.
- Недопустимые строки остаются в staging с заполненным `validation_error`.
""",
        "inputs/configuration/diagnostic-log.csv": """
sequence,hypothesis,check,observed_result,decision
1,,,,
2,,,,
3,,,,
4,,,,
5,,,,
""",
        "inputs/configuration/timeline-form.csv": """
timestamp,severity,component,event,observed_effect,causal_role,evidence_line
,,,,,,
,,,,,,
,,,,,,
,,,,,,
""",
        "inputs/configuration/test-matrix.csv": """
case_id,case_name,order_id,expected_property,actual_result,status,explanation
T01,Обычный заказ,1001,total equals manual calculation,,,
T02,Одна позиция,1004,no duplicate multiplication,,,
T03,Нет норм материалов,1007,material part equals zero,,,
T04,Несколько норм,1010,each norm counted once,,,
T05,Нулевое количество,9001,row is rejected or explicitly handled,,,
T06,Отрицательное количество,9002,row is rejected,,,
""",
        "inputs/configuration/procedure-contract.md": """
# Контракт процедуры `post_stock_movement`

Входы: `p_material_id`, `p_branch_id`, `p_quantity`, `p_movement_type`, `p_reference_no`.

Правила:

- материал и филиал должны существовать;
- количество строго больше нуля;
- тип — `RECEIPT` или `ISSUE`;
- выдача не может сделать остаток отрицательным;
- движение и остаток изменяются согласованно;
- при нарушении процедура завершает вызов через `SIGNAL SQLSTATE '45000'`;
- повторный `reference_no` не должен создавать второе движение.
""",
        "inputs/configuration/trigger-tests.csv": """
test_id,order_id,old_status,new_status,expected_audit_rows,actual_audit_rows,status
TR01,1001,NEW,NEW,0,,
TR02,1001,NEW,IN_PROGRESS,1,,
TR03,1001,IN_PROGRESS,DONE,1,,
TR04,1004,DONE,CANCELLED,1,,
""",
        "inputs/configuration/performance-protocol.csv": """
run,cache_state,rows_orders,rows_items,duration_ms,plan_root,rows_examined,notes
1,cold,,,,,,
2,warm,,,,,,
3,warm,,,,,,
4,warm,,,,,,
5,warm,,,,,,
median,warm,,,,,,
""",
        "inputs/configuration/index-comparison.csv": """
metric,before,after,delta,interpretation
Index definition,none,,,
Median duration ms,,,,
Rows examined,,,,
Plan access type,,,,
Extra storage KiB,,,,
Write-side effect,,,,
Decision,not applicable,,,keep/change/drop
""",
        "inputs/csv/orders_import.csv": """
external_order_no;branch_id;customer_id;order_date;quantity;status
EXT-2601;1;1;2026-02-03;2;NEW
EXT-2602;2;2;2026-02-05;1;IN_PROGRESS
EXT-2603;1;3;2026-02-08;4;DONE
EXT-2604;9;1;2026-02-10;1;NEW
EXT-2605;3;4;2026-02-30;2;NEW
EXT-2606;2;5;2026-02-12;0;NEW
EXT-2607;3;6;2026-02-14;3;UNKNOWN
EXT-2608;1;7;2026-03-01;6;DONE
EXT-2609;2;8;2026-03-04;51;NEW
EXT-2610;3;9;2026-03-07;2;CANCELLED
""",
        "inputs/security/privilege-matrix.csv": """
role,scope,allowed_operations,forbidden_test,user_prefix,host
service_reader,service_ops.*,SELECT,"INSERT INTO orders ...",reader,localhost
order_operator,service_ops.orders,"SELECT|INSERT|UPDATE(status)",DROP TABLE orders,operator,localhost
stock_operator,service_ops.stock_movements,"SELECT|INSERT",DELETE FROM stock_movements,stock,127.0.0.1
auditor,"service_ops.orders|service_ops.order_status_audit",SELECT,UPDATE orders SET status='DONE',auditor,localhost
""",
        "inputs/incidents/connection-cases.json": json.dumps([
            {"id": "C01", "clientError": "ERROR 2003 (HY000): Can't connect to MySQL server on '127.0.0.1:3311'", "fault": "service_stopped", "allowedChange": "start_service"},
            {"id": "C02", "clientError": "ERROR 2003 (HY000): Can't connect to MySQL server on '127.0.0.1:3306'", "fault": "wrong_client_port", "allowedChange": "client_port"},
            {"id": "C03", "clientError": "ERROR 1045 (28000): Access denied for user 'reader03'@'localhost'", "fault": "host_part_mismatch", "allowedChange": "account_host"},
            {"id": "C04", "clientError": "ERROR 2003 (HY000): Can't connect to MySQL server on '10.0.2.15:3314'", "fault": "bind_address", "allowedChange": "bind_address"},
            {"id": "C05", "clientError": "ERROR 3118 (HY000): Access denied for user 'reader05'@'localhost'. Account is locked.", "fault": "account_locked", "allowedChange": "unlock_account"},
            {"id": "C06", "clientError": "ERROR 1045 (28000): Access denied for user 'reader06'@'localhost'", "fault": "wrong_password", "allowedChange": "reset_training_password"}
        ], ensure_ascii=False, indent=2),
        "inputs/incidents/log-windows.csv": """
window_id,from,to,expected_component,noise_hint
W01,2026-02-12T09:14:00,2026-02-12T09:18:30,InnoDB,earlier authentication failures are unrelated
W02,2026-02-12T10:01:00,2026-02-12T10:05:00,Server,backup note is unrelated
W03,2026-02-12T11:42:00,2026-02-12T11:48:00,InnoDB,disk warning precedes failure
W04,2026-02-12T13:05:00,2026-02-12T13:10:00,Server,client disconnect is a consequence
W05,2026-02-12T14:20:00,2026-02-12T14:25:00,InnoDB,redo message is primary candidate
W06,2026-02-12T15:33:00,2026-02-12T15:38:00,Server,port collision is primary candidate
""",
        "inputs/logs/mysql-error-training.log": """
2026-02-12T09:12:04.011Z 8 [Warning] [MY-010055] [Server] IP address '10.0.2.19' could not be resolved
2026-02-12T09:14:48.205Z 0 [Note] [MY-012910] [InnoDB] Starting crash recovery
2026-02-12T09:15:10.448Z 0 [Warning] [MY-012638] [InnoDB] Retry attempts for reading a page failed
2026-02-12T09:15:11.017Z 0 [ERROR] [MY-013183] [InnoDB] Assertion failure in page validation; page 42:17
2026-02-12T09:15:11.022Z 0 [ERROR] [MY-010334] [Server] Failed to initialize DD Storage Engine
2026-02-12T09:15:11.024Z 0 [ERROR] [MY-010020] [Server] Data Dictionary initialization failed
2026-02-12T09:15:11.026Z 0 [ERROR] [MY-010119] [Server] Aborting
2026-02-12T10:00:02.110Z 0 [Note] [MY-010931] [Server] Ready for connections. Version: '8.4.0'
2026-02-12T10:02:44.782Z 22 [Warning] [MY-010055] [Server] Host name lookup failed for '10.0.2.55'
2026-02-12T10:03:12.013Z 0 [ERROR] [MY-000067] [Server] unknown variable 'max_connection=300'
2026-02-12T10:03:12.015Z 0 [ERROR] [MY-010119] [Server] Aborting
2026-02-12T11:42:17.101Z 0 [Warning] [MY-012149] [InnoDB] Disk is full writing './#innodb_redo/#ib_redo8_tmp'
2026-02-12T11:43:06.851Z 0 [ERROR] [MY-012267] [InnoDB] Unable to extend redo log file
2026-02-12T11:43:07.101Z 0 [ERROR] [MY-010334] [Server] Failed to initialize DD Storage Engine
2026-02-12T13:06:17.411Z 0 [ERROR] [MY-010262] [Server] Can't start server: Bind on TCP/IP port: Address already in use
2026-02-12T13:06:17.414Z 0 [ERROR] [MY-010119] [Server] Aborting
2026-02-12T14:21:31.210Z 0 [ERROR] [MY-013183] [InnoDB] Log sequence number is in the future
2026-02-12T14:21:31.216Z 0 [ERROR] [MY-010119] [Server] Aborting
2026-02-12T15:34:01.002Z 0 [ERROR] [MY-010262] [Server] Can't start server: Bind on TCP/IP port: Address already in use
2026-02-12T15:34:01.004Z 0 [ERROR] [MY-010119] [Server] Aborting
""",
        "inputs/sql/service_ops_schema.sql": """
-- MySQL 8.4. Выполняйте в базе своего варианта.
SET NAMES utf8mb4;
CREATE TABLE branches (
  branch_id INT PRIMARY KEY,
  branch_name VARCHAR(80) NOT NULL UNIQUE,
  city VARCHAR(80) NOT NULL
) ENGINE=InnoDB;
CREATE TABLE customers (
  customer_id BIGINT PRIMARY KEY,
  customer_name VARCHAR(120) NOT NULL,
  email VARCHAR(160) NOT NULL UNIQUE
) ENGINE=InnoDB;
CREATE TABLE services (
  service_id INT PRIMARY KEY,
  service_name VARCHAR(120) NOT NULL,
  unit_price DECIMAL(12,2) NOT NULL CHECK (unit_price >= 0)
) ENGINE=InnoDB;
CREATE TABLE materials (
  material_id INT PRIMARY KEY,
  material_name VARCHAR(120) NOT NULL,
  unit VARCHAR(20) NOT NULL,
  unit_price DECIMAL(12,2) NOT NULL CHECK (unit_price >= 0)
) ENGINE=InnoDB;
CREATE TABLE orders (
  order_id BIGINT PRIMARY KEY,
  external_order_no VARCHAR(30) UNIQUE,
  branch_id INT NOT NULL,
  customer_id BIGINT NOT NULL,
  order_date DATE NOT NULL,
  status ENUM('NEW','IN_PROGRESS','DONE','CANCELLED') NOT NULL DEFAULT 'NEW',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_orders_branch FOREIGN KEY (branch_id) REFERENCES branches(branch_id),
  CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
) ENGINE=InnoDB;
CREATE TABLE order_items (
  order_id BIGINT NOT NULL,
  line_no SMALLINT NOT NULL,
  service_id INT NOT NULL,
  quantity DECIMAL(10,2) NOT NULL CHECK (quantity > 0),
  PRIMARY KEY (order_id, line_no),
  CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
  CONSTRAINT fk_items_service FOREIGN KEY (service_id) REFERENCES services(service_id)
) ENGINE=InnoDB;
CREATE TABLE material_norms (
  service_id INT NOT NULL,
  material_id INT NOT NULL,
  quantity_per_service DECIMAL(10,3) NOT NULL CHECK (quantity_per_service >= 0),
  PRIMARY KEY (service_id, material_id),
  FOREIGN KEY (service_id) REFERENCES services(service_id),
  FOREIGN KEY (material_id) REFERENCES materials(material_id)
) ENGINE=InnoDB;
CREATE TABLE stock_movements (
  movement_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  material_id INT NOT NULL,
  branch_id INT NOT NULL,
  movement_type ENUM('RECEIPT','ISSUE') NOT NULL,
  quantity DECIMAL(12,3) NOT NULL CHECK (quantity > 0),
  reference_no VARCHAR(50) NOT NULL UNIQUE,
  occurred_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (material_id) REFERENCES materials(material_id),
  FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
) ENGINE=InnoDB;
CREATE TABLE material_balances (
  material_id INT NOT NULL,
  branch_id INT NOT NULL,
  quantity DECIMAL(12,3) NOT NULL DEFAULT 0 CHECK (quantity >= 0),
  PRIMARY KEY (material_id, branch_id),
  FOREIGN KEY (material_id) REFERENCES materials(material_id),
  FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
) ENGINE=InnoDB;
CREATE TABLE order_status_audit (
  audit_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  order_id BIGINT NOT NULL,
  old_status VARCHAR(20) NOT NULL,
  new_status VARCHAR(20) NOT NULL,
  changed_by VARCHAR(288) NOT NULL,
  changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
) ENGINE=InnoDB;
""",
        "inputs/sql/service_ops_seed.sql": """
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
""",
        "inputs/sql/staging_orders.sql": """
CREATE TABLE staging_orders (
  row_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  external_order_no VARCHAR(30), branch_id_text VARCHAR(20), customer_id_text VARCHAR(20),
  order_date_text VARCHAR(30), quantity_text VARCHAR(30), status_text VARCHAR(30),
  validation_error VARCHAR(500), loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Пример загрузки: адаптируйте абсолютный путь и параметры клиента.
LOAD DATA LOCAL INFILE 'ABSOLUTE_PATH/orders_import.csv'
INTO TABLE staging_orders CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n' IGNORE 1 LINES
(external_order_no, branch_id_text, customer_id_text, order_date_text, quantity_text, status_text);
""",
        "inputs/sql/privilege-tests.sql": """
-- Выполняйте каждый блок под указанной учебной учётной записью.
SELECT CURRENT_USER(), USER(), CURRENT_ROLE();
SELECT order_id, status FROM service_ops.orders ORDER BY order_id LIMIT 3;
INSERT INTO service_ops.stock_movements(material_id,branch_id,movement_type,quantity,reference_no)
VALUES (1,1,'RECEIPT',5,'PRIV-TEST-01');
UPDATE service_ops.orders SET status='IN_PROGRESS' WHERE order_id=1001;
DELETE FROM service_ops.stock_movements WHERE reference_no='PRIV-TEST-01';
DROP TABLE service_ops.orders;
""",
        "inputs/sql/join_case.sql": """
-- В запросе намеренно допущена ошибка соединения. Найдите её по кардинальности.
SELECT o.order_id, o.order_date, c.customer_name, b.branch_name
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
JOIN branches AS b ON b.branch_id = o.customer_id
ORDER BY o.order_id;
""",
        "inputs/sql/aggregation_case.sql": """
-- Детализация для самостоятельного построения агрегата.
SELECT o.order_id, o.branch_id, o.status, o.order_date,
       oi.quantity, s.unit_price, oi.quantity * s.unit_price AS service_amount
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN services s ON s.service_id = oi.service_id
WHERE o.order_date >= :date_from AND o.order_date < :date_to_exclusive;
""",
        "inputs/docs/calculation-rule.md": """
# Правило полной стоимости заказа

Полная стоимость = стоимость услуг + стоимость материалов.

- Стоимость услуг: сумма `order_items.quantity × services.unit_price`.
- Стоимость материалов: для каждой услуги `order_items.quantity × material_norms.quantity_per_service × materials.unit_price`.
- Сначала агрегируйте услуги и материалы отдельно до одного значения на `order_id`, затем соединяйте результаты.
- Отсутствующие нормы материалов дают нулевую материальную часть, но не удаляют заказ.
- Округление до двух знаков выполняется только в итоговом представлении.
""",
        "inputs/sql/full_order_cost_case.sql": """
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
""",
        "inputs/sql/calculation_boundary_cases.sql": """
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
""",
        "inputs/sql/procedure_case.sql": """
-- Набор вызовов; процедура создаётся студентом.
CALL post_stock_movement(1,1,10,'RECEIPT','CALL-OK-01');
CALL post_stock_movement(1,1,3,'ISSUE','CALL-OK-02');
CALL post_stock_movement(999,1,1,'RECEIPT','CALL-BAD-MATERIAL');
CALL post_stock_movement(1,1,0,'RECEIPT','CALL-BAD-ZERO');
CALL post_stock_movement(1,1,999999,'ISSUE','CALL-BAD-BALANCE');
CALL post_stock_movement(1,1,10,'RECEIPT','CALL-OK-01');
""",
        "inputs/sql/trigger_case.sql": """
-- После создания триггера выполняйте по одному UPDATE и проверяйте аудит.
SELECT COUNT(*) AS audit_before FROM order_status_audit WHERE order_id=1001;
UPDATE orders SET status=status WHERE order_id=1001;
UPDATE orders SET status='IN_PROGRESS' WHERE order_id=1001;
SELECT * FROM order_status_audit WHERE order_id=1001 ORDER BY audit_id;
""",
        "inputs/sql/slow_report.sql": """
-- Намеренно неэффективный учебный запрос. Не исправляйте до фиксации исходного плана.
SELECT o.order_id, o.order_date, b.branch_name, c.customer_name,
       SUM(oi.quantity * s.unit_price) AS service_amount
FROM orders o
JOIN branches b ON b.branch_id = o.branch_id
JOIN customers c ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN services s ON s.service_id = oi.service_id
WHERE YEAR(o.order_date) = 2026
  AND MONTH(o.order_date) BETWEEN 2 AND 6
  AND LOWER(b.branch_name) = LOWER('Центр')
GROUP BY o.order_id, o.order_date, b.branch_name, c.customer_name
ORDER BY o.order_date DESC, o.order_id;
""",
        "inputs/sql/generate_volume.sql": """
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
""",
        "inputs/capacity/workload-variants.csv": """
variant,current_data_gib,monthly_growth_gib,planning_months,active_share_pct,max_connections,per_connection_mib,daily_transfer_gib,peak_window_hours,retention_copies
1,120,12,18,30,180,4,38,6,2
2,250,18,24,25,260,5,65,8,2
3,80,9,36,40,140,4,30,5,3
4,420,28,18,20,350,6,95,8,2
5,160,15,30,35,220,5,52,7,3
6,300,21,24,30,300,6,78,6,2
""",
        "inputs/capacity/server-options.csv": """
option,cpu_cores,ram_gib,nvme_usable_gib,sustained_network_mbps,monthly_cost_units
A,8,32,1024,300,82
B,12,64,2048,600,128
C,16,96,4096,1000,196
""",
        "inputs/capacity/formulas.md": """
# Формулы учебной оценки

- Данные к концу периода: `current_data + monthly_growth × planning_months`.
- Диск с резервом: `projected_data × 1.35 + projected_data × 0.15 × retention_copies`.
- Рабочий набор: `projected_data × active_share_pct / 100`.
- Память: `working_set × 0.35 + max_connections × per_connection_MiB / 1024 + 8 GiB`.
- Сеть: `daily_transfer_GiB × 8192 / (peak_window_hours × 3600) × 1.4` Мбит/с.

Формулы — учебная модель. В выводе укажите, какое допущение сильнее всего меняет выбор.
""",
        "inputs/monitoring/prometheus.yml": """
global:
  scrape_interval: 15s
  evaluation_interval: 15s
scrape_configs:
  - job_name: mysql-training
    static_configs:
      - targets: ["EXPORTER_HOST:EXPORTER_PORT"]
        labels:
          environment: training
          instance_variant: VARIANT_ID
""",
        "inputs/monitoring/mysqld_exporter.my.cnf.example": """
[client]
user=monitoring_USER_SUFFIX
password=SET_LOCALLY_AND_DO_NOT_SUBMIT
host=127.0.0.1
port=MYSQL_PORT_FROM_VARIANT
""",
        "inputs/monitoring/required-metrics.md": """
# Контрольные вопросы и показатели

1. Доступен ли источник? — `up{job="mysql-training"}`.
2. Сколько подключений используется? — текущие подключения и настроенный предел.
3. Растёт ли объём операций? — счётчики команд или обработанных запросов как rate.
4. Есть ли риск нехватки диска? — свободное место файловой системы источника.

Названия экспортируемых серий зависят от версии exporter. В отчёте укажите фактическое имя, метки и запрос.
""",
        "inputs/monitoring/dashboard-starter.json": """
{
  "title": "UIABD — вариант VARIANT_ID",
  "timezone": "browser",
  "schemaVersion": 41,
  "tags": ["uiabd", "training"],
  "panels": [],
  "time": {"from": "now-6h", "to": "now"}
}
""",
        "inputs/monitoring/metrics.csv": """
timestamp,connections_used_pct,p95_query_seconds,disk_free_pct,error_rate_per_min
2026-08-18T09:00:00Z,22,0.18,43,0
2026-08-18T09:05:00Z,28,0.22,43,0
2026-08-18T09:10:00Z,35,0.31,42.8,1
2026-08-18T09:15:00Z,61,0.72,42.6,2
2026-08-18T09:20:00Z,79,1.44,42.4,5
2026-08-18T09:25:00Z,83,1.92,42.2,9
2026-08-18T09:30:00Z,68,0.88,42.1,3
2026-08-18T09:35:00Z,41,0.36,42.0,1
""",
        "inputs/monitoring/threshold-rules.csv": """
rule_id,metric,direction,warning,critical,window,required_samples
R01,connections_used_pct,above,65,80,5m,2
R02,p95_query_seconds,above,0.8,1.5,10m,2
R03,disk_free_pct,below,25,15,15m,3
R04,error_rate_per_min,above,3,8,5m,2
""",
        "inputs/monitoring/threshold-series.csv": """
timestamp,connections_used_pct,p95_query_seconds,disk_free_pct,error_rate_per_min,sample_state
2026-08-19T10:00:00Z,44,0.35,28,1,ok
2026-08-19T10:05:00Z,72,0.92,24,4,ok
2026-08-19T10:10:00Z,84,1.62,23,9,ok
2026-08-19T10:15:00Z,86,1.71,22,10,ok
2026-08-19T10:20:00Z,,,21,,missing
2026-08-19T10:25:00Z,63,0.77,20,2,ok
2026-08-19T10:30:00Z,51,0.42,14,1,ok
2026-08-19T10:35:00Z,49,0.38,14,1,ok
""",
        "inputs/incidents/metrics-incident.csv": """
timestamp,up,connections_used_pct,p95_query_seconds,disk_free_pct,error_rate_per_min
2026-08-20T14:00:00Z,1,48,0.42,19.2,1
2026-08-20T14:05:00Z,1,56,0.61,17.8,2
2026-08-20T14:10:00Z,1,73,1.08,15.3,5
2026-08-20T14:15:00Z,1,82,2.44,11.0,12
2026-08-20T14:20:00Z,0,,,9.7,
2026-08-20T14:25:00Z,0,,,9.7,
2026-08-20T14:30:00Z,1,12,0.31,27.4,0
""",
        "inputs/logs/mysql-incident.log": """
2026-08-20T14:08:12.094Z 0 [Warning] [MY-012149] [InnoDB] 805306368 bytes should have been written. Only 201326592 bytes written. Retrying.
2026-08-20T14:13:55.218Z 0 [Warning] [MY-012638] [InnoDB] Write retry attempts are increasing
2026-08-20T14:18:43.502Z 0 [ERROR] [MY-012267] [InnoDB] Unable to extend './#innodb_redo/#ib_redo9_tmp': No space left on device
2026-08-20T14:18:43.509Z 0 [ERROR] [MY-013183] [InnoDB] Redo log write failed
2026-08-20T14:18:43.514Z 0 [ERROR] [MY-010119] [Server] Aborting
2026-08-20T14:29:18.004Z 0 [Note] [MY-012910] [InnoDB] Starting crash recovery
2026-08-20T14:29:32.811Z 0 [Note] [MY-010931] [Server] Ready for connections. Version: '8.4.0'
""",
        "inputs/backup/service_ops_backup.sql": """
CREATE DATABASE IF NOT EXISTS service_ops_recovery CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE service_ops_recovery;
CREATE TABLE branches(branch_id INT PRIMARY KEY, branch_name VARCHAR(80) NOT NULL);
CREATE TABLE incident_orders(order_id BIGINT PRIMARY KEY, branch_id INT NOT NULL, status VARCHAR(20) NOT NULL, total DECIMAL(12,2) NOT NULL, FOREIGN KEY(branch_id) REFERENCES branches(branch_id));
INSERT INTO branches VALUES (1,'Центр'),(2,'Север'),(3,'Юг');
INSERT INTO incident_orders VALUES (7001,1,'DONE',15840.00),(7002,2,'IN_PROGRESS',9320.50),(7003,3,'NEW',22100.00),(7004,1,'DONE',4875.25),(7005,2,'CANCELLED',1100.00);
""",
        "inputs/sql/recovery_checks.sql": """
SELECT COUNT(*) AS tables_count FROM information_schema.tables WHERE table_schema='service_ops_recovery';
SELECT COUNT(*) AS branches_count FROM service_ops_recovery.branches;
SELECT COUNT(*) AS orders_count, ROUND(SUM(total),2) AS total_sum FROM service_ops_recovery.incident_orders;
SELECT branch_id, COUNT(*) AS order_count FROM service_ops_recovery.incident_orders GROUP BY branch_id ORDER BY branch_id;
CHECK TABLE service_ops_recovery.branches, service_ops_recovery.incident_orders;
""",
        "inputs/comparison/mysql_case.sql": """
CREATE DATABASE IF NOT EXISTS platform_case CHARACTER SET utf8mb4;
USE platform_case;
CREATE TABLE events(event_id BIGINT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(30) NOT NULL, happened_at TIMESTAMP NOT NULL, duration_ms INT NOT NULL CHECK(duration_ms >= 0));
INSERT INTO events(category,happened_at,duration_ms) VALUES ('read','2026-08-01 10:00:00',18),('write','2026-08-01 10:01:00',44),('read','2026-08-01 10:02:00',22),('read','2026-08-01 10:03:00',31);
CREATE ROLE platform_reader;
GRANT SELECT ON platform_case.* TO platform_reader;
SELECT category, COUNT(*) AS event_count, ROUND(AVG(duration_ms),2) AS avg_ms FROM events GROUP BY category ORDER BY category;
SELECT USER(), CURRENT_USER();
SHOW STATUS LIKE 'Threads_connected';
""",
        "inputs/comparison/postgresql_case.sql": """
CREATE SCHEMA platform_case;
CREATE TABLE platform_case.events(event_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, category VARCHAR(30) NOT NULL, happened_at TIMESTAMPTZ NOT NULL, duration_ms INTEGER NOT NULL CHECK(duration_ms >= 0));
INSERT INTO platform_case.events(category,happened_at,duration_ms) VALUES ('read','2026-08-01 10:00:00+00',18),('write','2026-08-01 10:01:00+00',44),('read','2026-08-01 10:02:00+00',22),('read','2026-08-01 10:03:00+00',31);
CREATE ROLE platform_reader NOLOGIN;
GRANT USAGE ON SCHEMA platform_case TO platform_reader;
GRANT SELECT ON platform_case.events TO platform_reader;
SELECT category, COUNT(*) AS event_count, ROUND(AVG(duration_ms),2) AS avg_ms FROM platform_case.events GROUP BY category ORDER BY category;
SELECT current_user, session_user;
SELECT state, COUNT(*) FROM pg_stat_activity GROUP BY state ORDER BY state;
""",
        "inputs/comparison/platform-matrix.csv": """
criterion,weight,mysql_fact,mysql_source_or_evidence,postgresql_fact,postgresql_source_or_evidence,score_mysql,score_postgresql
Installation and service,1,,,,,,
Roles and privileges,2,,,,,,
Data types and identity,1,,,,,,
Aggregate query,2,,,,,,
Connection monitoring,2,,,,,,
Priority from variant,3,,,,,,
Decision,not scored,,,,,,
""",
    }

    # Индивидуализация: каждая ситуационная работа получает 30 вариантов.
    collations = ["utf8mb4_0900_ai_ci", "utf8mb4_0900_as_ci", "utf8mb4_unicode_ci"]
    files["inputs/variants/c3-s6-variants.csv"] = csv_document(
        ["variant", "student_suffix", "service_name", "port", "datadir", "database_name", "collation", "reader_user", "operator_user", "allowed_host", "incident_case", "log_window"],
        [[index, f"{index:02d}", f"MySQL84_UIABD{index:02d}", 3310 + index, f"C:/mysql-data/uiabd{index:02d}", f"service_ops_{index:02d}", collations[(index - 1) % 3], f"reader{index:02d}", f"operator{index:02d}", "localhost" if index % 3 else "127.0.0.1", f"C{index:02d}", f"W{index:02d}"] for index in range(1, 31)],
    )
    statuses = ["NEW|IN_PROGRESS", "DONE|CANCELLED", "NEW|DONE", "IN_PROGRESS|DONE", "NEW|IN_PROGRESS|DONE"]
    files["inputs/variants/c4-s7-variants.csv"] = csv_document(
        ["variant", "branch_id", "date_from", "date_to", "statuses", "minimum_total", "order_id", "material_id", "slow_branch", "volume_rows"],
        [[index, 1 + (index - 1) % 3, f"2026-{2 + (index - 1) % 5:02d}-01", f"2026-{3 + (index - 1) % 5:02d}-28", statuses[(index - 1) % len(statuses)], 9000 + index * 750, 1001 + (index - 1) % 12, 1 + (index - 1) % 4, 1 + (index * 2) % 3, 20000 + index * 1000] for index in range(1, 31)],
    )
    metrics = ["connections_used_pct", "p95_query_seconds", "disk_free_pct", "error_rate_per_min"]
    priorities = ["reliability", "compatibility", "observability", "cost", "portability", "skills_available"]
    files["inputs/variants/c4-s8-variants.csv"] = csv_document(
        ["variant", "metric", "warning_threshold", "critical_threshold", "evaluation_window", "platform_priority", "incident_id"],
        [[index, metrics[(index - 1) % 4], 55 + (index % 6) * 3, 72 + (index % 6) * 3, f"{5 + (index % 3) * 5}m", priorities[(index - 1) % len(priorities)], f"I{index:02d}"] for index in range(1, 31)],
    )
    files["inputs/capacity/workload-variants.csv"] = csv_document(
        ["variant", "current_data_gib", "monthly_growth_gib", "planning_months", "active_share_pct", "max_connections", "per_connection_mib", "daily_transfer_gib", "peak_window_hours", "retention_copies"],
        [[index, 70 + index * 13, 7 + index % 11, 18 + (index % 4) * 6, 20 + (index % 5) * 5, 120 + index * 8, 4 + index % 3, 28 + index * 3, 5 + index % 4, 2 + index % 2] for index in range(1, 31)],
    )
    faults = [
        ("service_stopped", "start_service", "ERROR 2003 (HY000): Can't connect: service is not running"),
        ("wrong_client_port", "client_port", "ERROR 2003 (HY000): Can't connect to the configured TCP port"),
        ("host_part_mismatch", "account_host", "ERROR 1045 (28000): Access denied for the selected user@host"),
        ("bind_address", "bind_address", "ERROR 2003 (HY000): Remote address is not accepted"),
        ("account_locked", "unlock_account", "ERROR 3118 (HY000): Account is locked"),
        ("wrong_password", "reset_training_password", "ERROR 1045 (28000): Access denied with supplied credentials"),
    ]
    files["inputs/incidents/connection-cases.json"] = json.dumps([
        {"id": f"C{index:02d}", "variant": index, "clientError": faults[(index - 1) % len(faults)][2], "fault": faults[(index - 1) % len(faults)][0], "allowedChange": faults[(index - 1) % len(faults)][1], "serviceSuffix": f"{index:02d}", "expectedPort": 3310 + index}
        for index in range(1, 31)
    ], ensure_ascii=False, indent=2)
    files["inputs/incidents/log-windows.csv"] = csv_document(
        ["window_id", "variant", "from", "to", "expected_component", "noise_hint"],
        [[f"W{index:02d}", index, f"2026-02-{12 + (index - 1) // 6:02d}T{9 + (index - 1) % 6:02d}:{(index * 7) % 50:02d}:00", f"2026-02-{12 + (index - 1) // 6:02d}T{9 + (index - 1) % 6:02d}:{min(59, (index * 7) % 50 + 5):02d}:00", "InnoDB" if index % 2 else "Server", "Отделите первичную запись от фоновых предупреждений"] for index in range(1, 31)],
    )
    domains = [
        "мебельное производство", "производство светильников", "спортивное оборудование", "полиграфическая продукция", "учебные наборы",
        "сувенирная продукция", "садовая мебель", "текстильные изделия", "корпусная электроника", "велосипедные аксессуары",
        "детские конструкторы", "упаковочные материалы", "офисные перегородки", "кухонная посуда", "туристическое снаряжение",
        "лабораторная мебель", "рекламные конструкции", "системы хранения", "медицинские укладки", "театральные декорации",
        "торговое оборудование", "деревянные игрушки", "акустические панели", "защитные чехлы", "модульные стеллажи",
        "кабельные сборки", "настольные органайзеры", "выставочные стенды", "инструментальные тележки", "уличные навесы",
    ]
    product_terms = ["изделие", "модель", "комплект", "позиция", "продукт"]
    material_terms = ["материал", "компонент", "сырьё", "заготовка", "деталь"]
    files["inputs/demo-exam/kod-5-variants.csv"] = csv_document(
        ["variant", "enterprise_profile", "product_term", "material_term", "specification_term", "customer_term", "order_term", "database_name", "minimum_order_total"],
        [[index, domains[index - 1], product_terms[(index - 1) % 5], material_terms[(index - 1) % 5], f"спецификация_{index:02d}", "заказчик", "заказ", f"production_case_{index:02d}", 12000 + index * 900] for index in range(1, 31)],
    )
    files["inputs/demo-exam/kod-5-customers.json"] = json.dumps(
        {"description": "Учебный аналог файла Заказчики.json; выберите записи своего варианта", "variants": {f"{index:02d}": [
            {"customer_id": index * 100 + item, "name": f"Заказчик {index:02d}-{item}", "email": f"client{index:02d}{item}@example.test", "rating": 1 + (index + item) % 5}
            for item in range(1, 5)
        ] for index in range(1, 31)}},
        ensure_ascii=False,
        indent=2,
    )
    files["inputs/demo-exam/kod-5-api-cases.csv"] = csv_document(
        ["variant", "endpoint", "login", "note_title", "created_at", "expected_title_user", "expected_formatted_date", "required_tests"],
        [[index, "/api/notes" if index % 2 else "/notes", f"user{index:02d}", f"Заметка {index:02d}", f"2027-{1 + (index - 1) % 12:02d}-{1 + (index * 3) % 27:02d}", f"Заметка {index:02d} - user{index:02d}", f"{1 + (index * 3) % 27:02d}.{1 + (index - 1) % 12:02d}.2027", "200;500;valid JSON"] for index in range(1, 31)],
    )
    files["inputs/demo-exam/kod-5-evidence-manifest.csv"] = """
task,required_artifact,suggested_name,exists,independent_check,result
1,ER diagram,ER_VARIANT.pdf,,3NF; keys and relationships are readable,
2,database creation script,schema_VARIANT.sql,,creates an empty database without manual fixes,
2,JSON import script,import_customers_VARIANT.sql,,imports only the assigned variant and preserves identifiers,
3,full order cost query,full_cost_VARIANT.sql,,matches an independent calculation and avoids row multiplication,
4,information system module,app_VARIANT.zip,,authorization; captcha; lockout; administrator actions,
5,API source and test collection,api_VARIANT.zip,,GET notes; transformed JSON; tests 200 and 500 and JSON validity,
6,API documentation,api_documentation_VARIANT.docx,,base URL; methods; parameters; response format; HTTP codes,
all,short run guide,README_VARIANT.md,,expert can reproduce the sequence without oral comments,
"""
    files["inputs/demo-exam/kod-5-offline-rehearsal.md"] = """
# Интегрированная офлайн-репетиция КИМ 09.02.07-5-2027

Квалификация: **специалист по информационным системам**. Официальный комплект: <https://bom.firpo.ru/Public/6506>.

Материал является учебным аналогом заданий 1–6 и не заменяет официальные приложения КИМ. Номер варианта — 01–30 из `kod-5-variants.csv`; параметры API — из той же строки `kod-5-api-cases.csv`.

## Задание 1. ER-диаграмма — ориентир 20 минут

По предметной области своего варианта спроектируйте модель предприятия, которое производит продукцию по спецификациям, расходует материалы и принимает заказы клиентов. Обеспечьте 3НФ, ссылочную целостность, осмысленные имена, первичные и внешние ключи. Сохраните читаемую ER-диаграмму в PDF.

## Задание 2. Реализация базы и импорт JSON — ориентир 30 минут

На предпочтительной платформе создайте базу из собственной диаграммы: таблицы, типы, отношения и ограничения. Из `kod-5-customers.json` выберите массив своего варианта и импортируйте его отдельным воспроизводимым скриптом. Подтвердите число строк и два граничных идентификатора.

## Задание 3. Полная стоимость заказа — ориентир 20 минут

Создайте запрос полной стоимости заказа с учётом количества продукции, стоимости материалов и нормы расхода по спецификации. Не соединяйте две детализации без предварительной агрегации. Проверьте результат независимым расчётом для одного заказа и сценарием без одной из норм.

## Задание 4. Модуль информационной системы — ориентир 60 минут

Реализуйте учебный аналог технического задания: авторизация ролей «Администратор» и «Пользователь», обязательные логин и пароль, интерактивная капча-пазл, блокировка после трёх последовательных ошибок пароля или капчи, а также добавление, изменение и разблокировка пользователей администратором. Обработайте исключения и используйте осмысленные идентификаторы. Это задание выполняется на стыке с ПИДИС.

## Задание 5. API и автотесты — ориентир 60 минут

Создайте таблицу `notes`, связанную с `users`, и GET-эндпоинт из строки варианта. Ответ должен содержать `id`, `title_user` в формате «заголовок - логин», неизменённый `content` и `formatted_date` в формате ДД.ММ.ГГГГ. Реализуйте корректные ответы 400, пустой массив с 200 и сообщение с 500. Подготовьте коллекцию автоматизированных тестов: статус 200, статус 500 и валидность JSON.

## Задание 6. Документация API — ориентир 20 минут

Заполните документацию реализованного API: базовый URL, методы, параметры, описание, формат ответа и таблицу кодов HTTP. Документ должен соответствовать фактической реализации, а примеры — воспроизводиться без устных пояснений.

## Условия готовности

- Интернет и внешние подсказки не используются.
- Все артефакты сохраняются в папке варианта и перечисляются в `kod-5-evidence-manifest.csv`.
- Скрипты выполняются на пустой базе в однозначном порядке.
- Проверяющий воспроизводит результат без устных пояснений автора.
- Задания 4–6 проверяются как сквозная работа МДК.07.01, ПИДИС и интеграции программных модулей.
"""
    files["inputs/demo-exam/kod-5-readiness-checklist.md"] = """
# Матрица готовности к КИМ 09.02.07-5-2027

## Прямое покрытие — материалы МДК.07.01

- [ ] Задание 1: ER-диаграмма в 3НФ, читаемые сущности, атрибуты и ключи.
- [ ] Задание 2: база создаётся скриптом на выбранной платформе, JSON импортируется воспроизводимо.
- [ ] Задание 3: запрос полной стоимости учитывает количество продукции, материалы и нормы расхода.
- [ ] Результат каждого задания имеет независимую проверку и открывается без Интернета.
- [ ] Подготовлено 30 вариантов; студент работает только со своим номером.

## Сквозная готовность — ПИДИС и интеграция модулей

- [ ] Задание 4: авторизация, роли, капча-пазл, блокировка после трёх ошибок, администрирование пользователей и графический интерфейс.
- [ ] Задание 5: GET API заметок, преобразованный JSON, статусы 200/400/500 и автоматизированные тесты 200/500/валидность JSON.
- [ ] Задание 6: документация фактического API по официальной структуре — URL, методы, параметры, формат ответа и коды HTTP.
- [ ] Полная репетиция заданий 1–6 укладывается в 3 ч. 30 мин. без Интернета.

Мониторинг и инциденты 8 семестра развивают эксплуатационное мышление и поддерживают критерии соадминистрирования, но не засчитываются как замена прямым артефактам заданий 1–6.
"""

    for path, value in files.items():
        write(path, value)

    print(f"Generated {len(files)} input files")


if __name__ == "__main__":
    main()
