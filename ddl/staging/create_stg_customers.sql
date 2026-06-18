CREATE SCHEMA IF NOT EXISTS staging;
CREATE TABLE IF NOT EXISTS staging.customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(100),
    city VARCHAR(255),
    created_at VARCHAR(100)
)