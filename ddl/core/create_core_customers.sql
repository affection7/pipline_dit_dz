CREATE SCHEMA IF NOT EXISTS core;
CREATE TABLE IF NOT EXISTS core.customers (
    customer_id INTEGER PRIMARY KEY,
    full_name VARCHAR(50),
    email VARCHAR(50),
    phone VARCHAR(50),
    city VARCHAR(50),
    created_at DATE
);