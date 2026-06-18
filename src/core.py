import psycopg2
import os
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def execute_sql(cursor, path):
    with open(path, encoding='utf-8') as f:
        cursor.execute(f.read())
    print("Таблица успешно создана")

def load_table(cursor, table, df, columns):
    rows = df[columns].values.tolist()
    with open(f'./ddl/core/insert_core_{table}.sql', encoding='utf-8') as f:
        execute_values(cursor, f.read(), rows)
    return len(rows)

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

execute_sql(cursor, './ddl/core/create_core_customers.sql')
execute_sql(cursor, './ddl/core/create_core_products.sql')
execute_sql(cursor, './ddl/core/create_core_orders.sql')
execute_sql(cursor, './ddl/core/create_core_payments.sql')
execute_sql(cursor, './ddl/core/create_core_events.sql')

print("")

conn.commit()
cursor.close()
conn.close()