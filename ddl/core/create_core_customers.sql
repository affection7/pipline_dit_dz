CREATE SCHEMA IF NOT EXISTS core;
CREATE TABLE IF NOT EXISTS core.customers (
    customer_id INTEGER PRIMARY KEY,
    full_name VARCHAR(25),
    email VARCHAR(25),
    phone VARCHAR(15),
    city VARCHAR(25),
    created_at DATE
);