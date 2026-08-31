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
