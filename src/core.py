import psycopg2
import os
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from validate import clean_customers, clean_products, clean_orders, clean_payments, clean_events

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def execute_sql(cursor, path):
    with open(path, encoding='utf-8') as f:
        cursor.execute(f.read())
    print("Таблица успешно создана")

def load_table(cursor, table, df, columns):
    rows = df[columns].values.tolist()
    with open(f'./dml/core/insert_core_{table}.sql', encoding='utf-8') as f:
        execute_values(cursor, f.read(), rows)
    print(f"Успешно загружено {len(rows)} строк в таблицу {table}")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

execute_sql(cursor, './ddl/core/create_core_customers.sql')
execute_sql(cursor, './ddl/core/create_core_products.sql')
execute_sql(cursor, './ddl/core/create_core_orders.sql')
execute_sql(cursor, './ddl/core/create_core_payments.sql')
execute_sql(cursor, './ddl/core/create_core_events.sql')

load_table(cursor, 'customers', clean_customers(), ['customer_id', 'full_name', 'email', 'phone', 'city', 'created_at'])
load_table(cursor, 'products', clean_products(), ['product_id', 'product_name', 'category', 'price', 'currency', 'is_active'])
load_table(cursor, 'orders', clean_orders(), ['order_id', 'customer_id', 'product_id', 'quantity', 'unit_price', 'currency', 'order_timestamp', 'status'])
load_table(cursor, 'payments', clean_payments(), ['payment_id', 'order_id', 'payment_method', 'amount', 'currency', 'payment_timestamp'])
load_table(cursor, 'events', clean_events(), ['event_id', 'customer_id', 'event_type', 'event_timestamp', 'product_id'])

conn.commit()
cursor.close()
conn.close()