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
    sql_create_cus = f.read()
cursor.execute(sql_create_cus)

with open('./ddl/staging/create_stg_events.sql', encoding='utf-8') as f:
    sql_create_events = f.read()
cursor.execute(sql_create_events)

with open('./ddl/staging/create_stg_orders.sql', encoding='utf-8') as f:
    sql_create_orders = f.read()
cursor.execute(sql_create_orders)

with open('./ddl/staging/create_stg_payments.sql', encoding='utf-8') as f:
    sql_create_pay = f.read()
cursor.execute(sql_create_pay)

with open('./ddl/staging/create_stg_products.sql', encoding='utf-8') as f:
    sql_create_prod = f.read()
cursor.execute(sql_create_prod)



df_cust = pd.read_csv('./data/customers.csv', sep=',')
rows_cust = df_cust[['customer_id', 'full_name', 'email', 'phone', 'city', 'created_at']].values.tolist()

sql_insert_cust = './ddl/staging/insert_stg_customers.sql'

with open(sql_insert_cust, encoding='utf-8') as f:
    sql_insert = f.read()

execute_values(cursor, sql_insert, rows_cust)

df_orders = pd.read_json('./data/orders.json')
rows_orders= df_orders[['order_id', 'customer_id', 'product_id', 'quantity', 'unit_price', 'currency', 'order_timestamp', 'status']].values.tolist()

sql_insert_orders= './ddl/staging/insert_stg_orders.sql'

with open(sql_insert_orders, encoding='utf-8') as f:
    sql_insert_orders = f.read()

execute_values(cursor, sql_insert_orders, rows_orders)

df_pay = pd.read_csv('./data/payments.csv', sep='^')
rows_pay= df_pay[['payment_id', 'order_id', 'payment_method', 'amount', 'currency', 'payment_timestamp']].values.tolist()

sql_insert_pay= './ddl/staging/insert_stg_payments.sql'

with open(sql_insert_pay, encoding='utf-8') as f:
    sql_insert_pay = f.read()

execute_values(cursor, sql_insert_pay, rows_pay)

conn.commit()
cursor.close()
conn.close()

print(f"Успешно загружено {len(rows_cust)} строк в таблицу customers")
print(f"Успешно загружено {len(rows_orders)} строк в таблицу  orders")
print(f"Успешно загружено {len(rows_pay)} строк в таблицу  payments")
