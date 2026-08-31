CREATE DATABASE IF NOT EXISTS service_ops_recovery CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE service_ops_recovery;
CREATE TABLE branches(branch_id INT PRIMARY KEY, branch_name VARCHAR(80) NOT NULL);
CREATE TABLE incident_orders(order_id BIGINT PRIMARY KEY, branch_id INT NOT NULL, status VARCHAR(20) NOT NULL, total DECIMAL(12,2) NOT NULL, FOREIGN KEY(branch_id) REFERENCES branches(branch_id));
INSERT INTO branches VALUES (1,'Центр'),(2,'Север'),(3,'Юг');
INSERT INTO incident_orders VALUES (7001,1,'DONE',15840.00),(7002,2,'IN_PROGRESS',9320.50),(7003,3,'NEW',22100.00),(7004,1,'DONE',4875.25),(7005,2,'CANCELLED',1100.00);
