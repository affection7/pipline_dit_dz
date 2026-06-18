import pandas as pd
import psycopg2
import os
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_IP = os.getenv("DB_IP")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}"

def execute_sql(cursor, file_path):
    with open(file_path, encoding='utf-8') as f:
        cursor.execute(f.read())

def load_table(cursor, table_name, df, columns):
    """fdfefefwef"""
    rows = df[columns].values.tolist()
    df.columns
    with open(f'./dml/staging/insert_stg_{table_name}.sql', encoding='utf-8') as f:
        execute_values(cursor, f.read(), rows)
    print(f"Успешно загружено {len(rows)} строк в таблицу {table_name}")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

execute_sql(cursor, './ddl/staging/create_stg_customers.sql')
execute_sql(cursor, './ddl/staging/create_stg_events.sql')
execute_sql(cursor, './ddl/staging/create_stg_orders.sql')
execute_sql(cursor, './ddl/staging/create_stg_payments.sql')
execute_sql(cursor, './ddl/staging/create_stg_products.sql')

cursor.execute("TRUNCATE TABLE staging.customers, staging.events, staging.orders, staging.payments, staging.products CASCADE;")
conn.commit()

load_table(cursor, 'customers', pd.read_csv('./data/customers.csv', sep=','),['customer_id', 'full_name', 'email', 'phone', 'city', 'created_at'])

load_table(cursor, 'orders', pd.read_json('./data/orders.json'),['order_id', 'customer_id', 'product_id', 'quantity', 'unit_price', 'currency', 'order_timestamp', 'status'])

load_table(cursor, 'payments', pd.read_csv('./data/payments.csv', sep='^'),['payment_id', 'order_id', 'payment_method', 'amount', 'currency', 'payment_timestamp'])

load_table(cursor, 'products', pd.read_excel('./data/products.xlsx', sheet_name='products'),['product_id', 'product_name', 'category', 'price', 'currency', 'is_active'])

load_table(cursor, 'events', pd.read_xml('./data/events.xml'),['event_id', 'customer_id', 'event_type', 'event_timestamp', 'product_id'])

conn.commit()
cursor.close()
conn.close()