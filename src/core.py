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

def filter_df(df, column, valid_values, msg):
    before = len(df)
    df = df[df[column].isin(valid_values)]
    dropped = before - len(df)

    if dropped:
        logging.warning(f"{msg}: отброшено {dropped} строк")

    return df

def get_clean(table, cleaner, cursor):
    df = read_staging_table(cursor, table)
    return cleaner(df)

def run_core():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    ddl_files = [
        './ddl/core/create_core_customers.sql',
        './ddl/core/create_core_products.sql',
        './ddl/core/create_core_orders.sql',
        './ddl/core/create_core_payments.sql',
        './ddl/core/create_core_events.sql',
    ]

    for path in ddl_files:
        execute_sql(cursor, path)

    customers = get_clean('customers', clean_customers, cursor)
    load_table(cursor, 'customers', customers)
    valid_customer_ids = set(customers['customer_id'])

    products = get_clean('products', clean_products, cursor)
    load_table(cursor, 'products', products)
    valid_product_ids = set(products['product_id'])

    orders = get_clean('orders', clean_orders, cursor)

    orders = filter_df(
        orders,
        'customer_id',
        valid_customer_ids,
        "orders: нет customer_id"
    )

    orders = filter_df(
        orders,
        'product_id',
        valid_product_ids,
        "orders: нет product_id"
    )

    load_table(cursor, 'orders', orders)
    valid_order_ids = set(orders['order_id'].astype(int))

    payments = get_clean('payments', clean_payments, cursor)
    payments['order_id'] = payments['order_id'].astype(int)

    payments = filter_df(
        payments,
        'order_id',
        valid_order_ids,
        "payments: нет order_id"
    )

    load_table(cursor, 'payments', payments)

    events = get_clean('events', clean_events, cursor)

    events['product_id'] = events['product_id'].astype(float).astype(int)
    events['customer_id'] = events['customer_id'].astype(float).astype(int)

    events = filter_df(
        events,
        'customer_id',
        set(map(int, valid_customer_ids)),
        "events: нет customer_id"
    )

    events = filter_df(
        events,
        'product_id',
        set(map(int, valid_product_ids)),
        "events: нет product_id"
    )

    load_table(cursor, 'events', events)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    run_core()