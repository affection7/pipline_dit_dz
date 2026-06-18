CREATE SCHEMA IF NOT EXISTS core;
CREATE TABLE IF NOT EXISTS core.products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(25),
    price DECIMAL(10,2),
    currency VARCHAR(10),
    is_active BOOLEAN
);