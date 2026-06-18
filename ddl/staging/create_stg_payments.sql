CREATE SCHEMA IF NOT EXISTS staging;
CREATE TABLE IF NOT EXISTS staging.payments (
    payment_id VARCHAR(50),
    order_id VARCHAR(50),
    payment_method VARCHAR(100),
    amount VARCHAR(50),
    currency VARCHAR(20),
    payment_timestamp VARCHAR(100)
)