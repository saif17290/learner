import sqlite3
from contextlib import contextmanager
from typing import Iterator

import pandas as pd


@contextmanager
def get_connection(db_path: str = 'db/orders.db') -> Iterator[sqlite3.Connection]:
    """Context manager returning a sqlite3 connection and ensuring it's closed."""
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def query_to_df(sql: str, db_path: str = 'db/orders.db') -> pd.DataFrame:
    """Run a SQL query and return results as a pandas DataFrame."""
    with get_connection(db_path) as conn:
        return pd.read_sql_query(sql, conn)


def fetch_orders(limit: int = 100, db_path: str = 'db/orders.db') -> pd.DataFrame:
    """Return up to `limit` rows from the `orders_clean` table."""
    sql = f"SELECT * FROM orders_clean ORDER BY order_id LIMIT {limit}"
    return query_to_df(sql, db_path)
