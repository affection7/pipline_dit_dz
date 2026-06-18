CREATE SCHEMA IF NOT EXISTS core;
CREATE TABLE IF NOT EXISTS core.payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    payment_method VARCHAR(25),
    amount DECIMAL(10,2),
    currency VARCHAR(10),
    payment_timestamp TIMESTAMP,
    CONSTRAINT fk_payments_order FOREIGN KEY (order_id) REFERENCES core.orders(order_id)
);