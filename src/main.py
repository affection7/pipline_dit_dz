import pandas as pd
import psycopg2
import os
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

with open('./ddl/staging/create_stg_customers.sql', encoding='utf-8') as f:
    cursor.execute(f.read())

with open('./ddl/staging/create_stg_events.sql', encoding='utf-8') as f:
    cursor.execute(f.read())

with open('./ddl/staging/create_stg_orders.sql', encoding='utf-8') as f:
    cursor.execute(f.read())

with open('./ddl/staging/create_stg_payments.sql', encoding='utf-8') as f:
    cursor.execute(f.read())

with open('./ddl/staging/create_stg_products.sql', encoding='utf-8') as f:
    cursor.execute(f.read())

cursor.execute("""
    TRUNCATE TABLE staging.customers,staging.events,staging.orders,staging.payments,staging.products CASCADE;
               """)
conn.commit()

df_cust = pd.read_csv('./data/customers.csv', sep=',')
rows_cust = df_cust[['customer_id', 'full_name', 'email', 'phone', 'city', 'created_at']].values.tolist()

with open('./ddl/staging/insert_stg_customers.sql', encoding='utf-8') as f:
    sql_insert_cust = f.read()

execute_values(cursor, sql_insert_cust, rows_cust)
print(f"Успешно загружено {len(rows_cust)} строк в таблицу customers")

df_orders = pd.read_json('./data/orders.json')
rows_orders = df_orders[['order_id', 'customer_id', 'product_id', 'quantity', 'unit_price', 'currency', 'order_timestamp', 'status']].values.tolist()

with open('./ddl/staging/insert_stg_orders.sql', encoding='utf-8') as f:
    sql_insert_orders = f.read()

execute_values(cursor, sql_insert_orders, rows_orders)
print(f"Успешно загружено {len(rows_orders)} строк в таблицу orders")

df_pay = pd.read_csv('./data/payments.csv', sep='^')
rows_pay = df_pay[['payment_id', 'order_id', 'payment_method', 'amount', 'currency', 'payment_timestamp']].values.tolist()

with open('./ddl/staging/insert_stg_payments.sql', encoding='utf-8') as f:
    sql_insert_pay = f.read()

execute_values(cursor, sql_insert_pay, rows_pay)
print(f"Успешно загружено {len(rows_pay)} строк в таблицу payments")

df_prod = pd.read_excel('./data/products.xlsx', sheet_name='products')
rows_prod = df_prod[['product_id', 'product_name', 'category', 'price', 'currency', 'is_active']].values.tolist()

with open('./ddl/staging/insert_stg_products.sql', encoding='utf-8') as f:
    sql_insert_prod = f.read()

execute_values(cursor, sql_insert_prod, rows_prod)
print(f"Успешно загружено {len(rows_prod)} строк в таблицу products")


df_events = pd.read_xml('./data/events.xml')
df_events = df_events.drop_duplicates(subset=['event_id'])
rows_events = df_events[['event_id', 'customer_id', 'event_type', 'event_timestamp', 'product_id']].values.tolist()

with open('./ddl/staging/insert_stg_events.sql', encoding='utf-8') as f:
    sql_insert_events = f.read()

execute_values(cursor, sql_insert_events, rows_events)
print(f"Успешно загружено {len(rows_events)} строк в таблицу events")

conn.commit()
cursor.close()
conn.close()