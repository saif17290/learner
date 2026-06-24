import csv
import os
import random
import sqlite3
from datetime import datetime, timedelta

import pandas as pd


def _ensure_raw_exists(path: str, n: int = 30) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        return

    products = ['widget', 'gadget', 'doodad', 'thingamajig']
    start = datetime.today() - timedelta(days=365)

    rows = []
    for i in range(1, n + 1):
        order_date = (start + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        product = random.choice(products)
        # mostly numbers, but insert empty string sometimes to simulate dirty data
        if random.random() < 0.15:
            quantity = ''
        else:
            quantity = random.randint(1, 5)
        unit_price = round(random.uniform(5.0, 200.0), 2)
        rows.append([i, order_date, product, quantity, unit_price])

    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['order_id', 'order_date', 'product', 'quantity', 'unit_price'])
        for r in rows:
            writer.writerow(r)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # treat empty strings as missing
    df['quantity'] = df['quantity'].replace('', pd.NA)
    df['quantity'] = df['quantity'].fillna(1)
    df['quantity'] = df['quantity'].astype(int)
    df['unit_price'] = df['unit_price'].astype(float)
    df['revenue'] = df['quantity'] * df['unit_price']
    return df


def load(df: pd.DataFrame, output_csv: str = 'data/processed/orders_clean.csv', db_path: str = 'db/orders.db') -> None:
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    df.to_csv(output_csv, index=False)

    # write to SQLite, replacing table
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS orders_clean')
    cur.execute(
        'CREATE TABLE orders_clean(order_id INTEGER PRIMARY KEY, order_date TEXT, product TEXT, quantity INTEGER, unit_price REAL, revenue REAL)'
    )
    insert_sql = 'INSERT INTO orders_clean(order_id, order_date, product, quantity, unit_price, revenue) VALUES (?, ?, ?, ?, ?, ?)'
    rows = [(
        int(r['order_id']),
        str(r['order_date']),
        str(r['product']),
        int(r['quantity']),
        float(r['unit_price']),
        float(r['revenue']),
    ) for _, r in df.iterrows()]
    cur.executemany(insert_sql, rows)
    conn.commit()
    conn.close()


def run(raw_path: str = 'data/raw/orders.csv', processed_path: str = 'data/processed/orders_clean.csv', db_path: str = 'db/orders.db') -> None:
    _ensure_raw_exists(raw_path)
    df = pd.read_csv(raw_path)
    cleaned = transform(df)
    load(cleaned, processed_path, db_path)

    total_orders = len(cleaned)
    total_revenue = cleaned['revenue'].sum()
    top_product = cleaned.groupby('product')['revenue'].sum().idxmax()

    print(f'total_orders: {total_orders}')
    print(f'total_revenue: {total_revenue}')
    print(f'top_product_by_revenue: {top_product}')


if __name__ == '__main__':
    run()
