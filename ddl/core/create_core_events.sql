CREATE SCHEMA IF NOT EXISTS core;
CREATE TABLE IF NOT EXISTS core.events (
    event_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    event_type VARCHAR(25),
    event_timestamp TIMESTAMP,
    product_id VARCHAR(50),
    CONSTRAINT fk_events_customer FOREIGN KEY (customer_id) REFERENCES core.customers(customer_id),
    CONSTRAINT fk_events_product FOREIGN KEY (product_id) REFERENCES core.products(product_id)
);