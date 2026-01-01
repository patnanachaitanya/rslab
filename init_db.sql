CREATE DATABASE IF NOT EXISTS sqli_lab;
USE sqli_lab;

DROP TABLE IF EXISTS orders, customers;

CREATE TABLE customers (id INT PRIMARY KEY AUTO_INCREMENT, email VARCHAR(100));
CREATE TABLE orders (id INT PRIMARY KEY AUTO_INCREMENT, tracking_id VARCHAR(20) UNIQUE, customer_id INT);

INSERT INTO customers (email) VALUES ('test@shop.com');
INSERT INTO orders (tracking_id, customer_id) VALUES ('ORD-12345', 1);