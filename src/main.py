import pandas as pd
import psycopg2
import os
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

with open('./ddl/staging/create_stg_customers.sql', encoding='utf-8') as f:
    sql_create = f.read()

df = pd.read_csv('./data/customers.csv')

rows = df[['customer_id', 'full_name', 'email', 'phone', 'city', 'created_at']].values.tolist()

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute(sql_create)

sql_insert = './ddl/staging/insert_stg_customers.sql'

with open(sql_insert, encoding='utf-8') as f:
    sql_insert = f.read()


execute_values(cursor, sql_insert, rows)

conn.commit()
cursor.close()
conn.close()

print(f"Успешно загружено {len(rows)} строк")
