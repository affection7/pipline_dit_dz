CREATE SCHEMA IF NOT EXISTS core;
CREATE TABLE IF NOT EXISTS core.orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    currency VARCHAR(10),
    order_timestamp TIMESTAMP,
    status VARCHAR(50),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES core.customers(customer_id),
    CONSTRAINT fk_orders_product FOREIGN KEY (product_id) REFERENCES core.products(product_id)
);