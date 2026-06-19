import pandas as pd

def remove_duplicates(df, subset):
    return df.drop_duplicates(subset=subset, keep='last')

def cast_numeric(df, column):
    df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

def cast_timestamp(df, column, fmt=None):
    df[column] = pd.to_datetime(df[column], format=fmt, errors='coerce')
    df[column] = df[column].where(pd.notna(df[column]), None).astype(object)
    return df

def drop_invalid(df, subset):
    return df.dropna(subset=subset)

def normalize_nulls(df):
    return df.where(pd.notnull(df), None)

def clean_customers(df):
    df = remove_duplicates(df, subset=['customer_id'])
    df = cast_numeric(df, 'customer_id')
    df = drop_invalid(df, subset=['customer_id'])

    df['full_name'] = df['full_name'].str.strip()
    
    df['phone'] = df['phone'].replace('UNKNOWN', pd.NA)
    df['phone'] = df['phone'].replace('', pd.NA)

    df['email'] = df['email'].replace('', pd.NA)

    df = cast_timestamp(df, 'created_at', fmt='%Y-%m-%d')
    return normalize_nulls(df)


def clean_orders(df):
    df = remove_duplicates(df, subset=['order_id'])
    df = cast_numeric(df, 'customer_id')
    df = drop_invalid(df, subset=['customer_id'])

    df = cast_timestamp(df, 'order_timestamp')
    df = drop_invalid(df, subset=['order_timestamp'])

    df = cast_numeric(df, 'quantity')
    df = cast_numeric(df, 'unit_price')
    df = drop_invalid(df, subset=['quantity', 'unit_price'])
    df = df[df['quantity'] > 0]
    df = df[df['unit_price'] > 0]

    return normalize_nulls(df)


def clean_payments(df):
    df = remove_duplicates(df, subset=['payment_id'])
    df = cast_numeric(df, 'order_id')
    df = drop_invalid(df, subset=['order_id'])

    df['amount'] = df['amount'].replace('error_amount', pd.NA)
    df = cast_numeric(df, 'amount')
    df = drop_invalid(df, subset=['amount'])
    df = df[df['amount'] > 0]

    df['payment_method'] = df['payment_method'].replace('', pd.NA)

    df = cast_timestamp(df, 'payment_timestamp')
    df = drop_invalid(df, subset=['payment_timestamp'])

    return normalize_nulls(df)


def clean_products(df):
    df = remove_duplicates(df, subset=['product_id'])

    df['product_name'] = df['product_name'].str.strip()

    df['price'] = df['price'].astype(str).str.replace(',', '.', regex=False)
    df['price'] = df['price'].replace('N/A', pd.NA)
    df = cast_numeric(df, 'price')
    df = drop_invalid(df, subset=['price'])
    df = df[df['price'] > 0]

    df['is_active'] = df['is_active'].map({'ИСТИНА': True, 'ЛОЖЬ': False})

    return normalize_nulls(df)


def clean_events(df):
    df = remove_duplicates(df, subset=['event_id'])
    df = cast_numeric(df, 'customer_id')
    df = drop_invalid(df, subset=['customer_id'])

    df = cast_timestamp(df, 'event_timestamp')
    df = drop_invalid(df, subset=['event_timestamp'])
    return normalize_nulls(df)