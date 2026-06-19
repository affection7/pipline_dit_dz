import psycopg2
import os
import pandas as pd
import logging
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from validate import clean_customers, clean_products, clean_orders, clean_payments, clean_events

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_IP = os.getenv("DB_IP")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}"

def execute_sql(cursor, path):
    with open(path, encoding='utf-8') as f:
        cursor.execute(f.read())
    logging.info(f"Таблица успешно создана: {path}")

def load_table(cursor, table, df):
    rows = df.values.tolist()
    with open(f'./dml/core/insert_core_{table}.sql', encoding='utf-8') as f:
        execute_values(cursor, f.read(), rows)
    logging.info(f"Успешно загружено {len(rows)} строк в таблицу {table}")

def read_staging_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM staging.{table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(rows, columns=columns)

def run_core():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    execute_sql(cursor, './ddl/core/create_core_customers.sql')
    execute_sql(cursor, './ddl/core/create_core_products.sql')
    execute_sql(cursor, './ddl/core/create_core_orders.sql')
    execute_sql(cursor, './ddl/core/create_core_payments.sql')
    execute_sql(cursor, './ddl/core/create_core_events.sql')

    df = read_staging_table(cursor, 'customers')
    df = clean_customers(df)
    load_table(cursor, 'customers', df)
    valid_customer_ids = set(df['customer_id'])

    df = read_staging_table(cursor, 'products')
    df = clean_products(df)
    load_table(cursor, 'products', df)
    valid_product_ids = set(df['product_id'])

    df = read_staging_table(cursor, 'orders')
    df = clean_orders(df)

    before = len(df)
    df = df[df['customer_id'].isin(valid_customer_ids)]
    dropped = before - len(df)
    if dropped:
        logging.warning(f"orders: отброшено {dropped} строк — customer_id не найден в core.customers")

    before = len(df)
    df = df[df['product_id'].isin(valid_product_ids)]
    dropped = before - len(df)
    if dropped:
        logging.warning(f"orders: отброшено {dropped} строк — product_id не найден в core.products")

    load_table(cursor, 'orders', df)
    valid_order_ids = set(df['order_id'].astype(int))

    df = read_staging_table(cursor, 'payments')
    df = clean_payments(df)
    df['order_id'] = df['order_id'].astype(int)

    before = len(df)
    df = df[df['order_id'].isin(valid_order_ids)]
    dropped = before - len(df)
    if dropped:
        logging.warning(f"payments: отброшено {dropped} строк — order_id не найден в core.orders")

    load_table(cursor, 'payments', df)

    df = read_staging_table(cursor, 'events')
    df = clean_events(df)
    df['product_id'] = df['product_id'].astype(float).astype(int)
    df['customer_id'] = df['customer_id'].astype(float).astype(int)

    before = len(df)
    df = df[df['customer_id'].isin({int(x) for x in valid_customer_ids})]
    dropped = before - len(df)
    if dropped:
        logging.warning(f"events: отброшено {dropped} строк — customer_id не найден в core.customers")

    before = len(df)
    df = df[df['product_id'].isin({int(x) for x in valid_product_ids})]
    dropped = before - len(df)
    if dropped:
        logging.warning(f"events: отброшено {dropped} строк — product_id не найден в core.products")

    load_table(cursor, 'events', df)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    run_core()