CREATE SCHEMA IF NOT EXISTS staging;
CREATE TABLE IF NOT EXISTS staging.orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity VARCHAR(50),
    unit_price VARCHAR(50),
    currency VARCHAR(20),
    order_timestamp VARCHAR(100),
    status VARCHAR(100)
)