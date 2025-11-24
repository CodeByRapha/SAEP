create database saep_db;

use saep_db;

CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    stock INT DEFAULT 0,
    min_stock INT DEFAULT 0,
    storage VARCHAR(100)
);

CREATE TABLE stockmovement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    movement_type CHAR(1) NOT NULL,
    quantity INT NOT NULL,
    performed_by VARCHAR(100),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- Inserção de 3 registros mínimos, conforme pedido da prova
INSERT INTO product (name, description, stock, min_stock, storage) VALUES
('Smartphone X Pro', 'Smartphone de teste', 10, 3, '128GB'),
('Notebook Alpha 15', 'Notebook de teste', 5, 2, '512GB SSD'),
('Smart TV Vision 42', 'TV de teste', 2, 1, 'N/A');

INSERT INTO stockmovement (product_id, movement_type, quantity, performed_by, notes) VALUES
(1, 'E', 5, 'admin', 'Entrada inicial'),
(2, 'S', 1, 'admin', 'Saída de teste'),
(3, 'E', 3, 'admin', 'Reposição de estoque');
