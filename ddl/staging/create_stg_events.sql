CREATE SCHEMA IF NOT EXISTS staging;
CREATE TABLE IF NOT EXISTS staging.events (
    event_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    event_type VARCHAR(100),
    event_timestamp VARCHAR(100),
    product_id VARCHAR(50)
)