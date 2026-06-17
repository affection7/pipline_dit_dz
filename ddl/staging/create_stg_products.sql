CREATE TABLE IF NOT EXISTS staging.products (
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    category VARCHAR(255),
    price VARCHAR(50),
    currency VARCHAR(20),
    is_active VARCHAR(50)
);