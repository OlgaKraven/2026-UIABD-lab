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
LINES TERMINATED BY '
' IGNORE 1 LINES
(external_order_no, branch_id_text, customer_id_text, order_date_text, quantity_text, status_text);
