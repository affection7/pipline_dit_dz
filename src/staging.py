import pandas as pd
import psycopg2
import os
import logging
from psycopg2.extras import execute_values
from dotenv import load_dotenv

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

def load_table(cursor, table_name, df):
    rows = df.values.tolist()
    with open(f'./dml/staging/insert_stg_{table_name}.sql', encoding='utf-8') as f:
        execute_values(cursor, f.read(), rows)
    logging.info(f"Успешно загружено {len(rows)} строк в таблицу {table_name}")

def run_staging():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    execute_sql(cursor, './ddl/staging/create_stg_customers.sql')
    execute_sql(cursor, './ddl/staging/create_stg_events.sql')
    execute_sql(cursor, './ddl/staging/create_stg_orders.sql')
    execute_sql(cursor, './ddl/staging/create_stg_payments.sql')
    execute_sql(cursor, './ddl/staging/create_stg_products.sql')

    cursor.execute("TRUNCATE TABLE staging.customers, staging.events, staging.orders, staging.payments, staging.products CASCADE;")
    conn.commit()

    load_table(cursor, 'customers', pd.read_csv('./data/customers.csv', sep=','))
    load_table(cursor, 'orders', pd.read_json('./data/orders.json'))
    load_table(cursor, 'payments', pd.read_csv('./data/payments.csv', sep='^'))
    load_table(cursor, 'products', pd.read_excel('./data/products.xlsx', sheet_name='products'))
    load_table(cursor, 'events', pd.read_xml('./data/events.xml'))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    run_staging()