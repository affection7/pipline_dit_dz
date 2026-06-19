import psycopg2
import os
import pandas as  pd
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
    print("Таблица успешно создана")

def load_table(cursor, table, df):
    rows = df.values.tolist()
    with open(f'./dml/core/insert_core_{table}.sql', encoding='utf-8') as f:
        execute_values(cursor, f.read(), rows)
    print(f"Успешно загружено {len(rows)} строк в таблицу {table}")

def read_staging_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM staging.{table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(rows, columns=columns)

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

df = read_staging_table(cursor, 'orders')
df = clean_orders(df)
load_table(cursor, 'orders', df)

df = read_staging_table(cursor, 'payments')
df = clean_payments(df)
load_table(cursor, 'payments', df)

df = read_staging_table(cursor, 'products')
df = clean_products(df)
load_table(cursor, 'products', df)

df = read_staging_table(cursor, 'events')
df = clean_events(df)
load_table(cursor, 'events', df)

conn.commit()
cursor.close()
conn.close()