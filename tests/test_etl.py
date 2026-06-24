import pandas as pd
import numpy as np
from src.etl import transform


def test_revenue_column_exists_and_non_negative():
    df = pd.DataFrame({
        'order_id': [1, 2, 3],
        'order_date': ['2026-01-01', '2026-01-02', '2026-01-03'],
        'product': ['a', 'b', 'c'],
        'quantity': [2, 1, 3],
        'unit_price': [10.0, 5.5, 2.0]
    })
    out = transform(df)
    assert 'revenue' in out.columns
    assert (out['revenue'] >= 0).all()


def test_missing_quantity_filled_with_one():
    df = pd.DataFrame({
        'order_id': [1, 2, 3],
        'order_date': ['2026-01-01', '2026-01-02', '2026-01-03'],
        'product': ['a', 'b', 'c'],
        'quantity': [np.nan, '', 5],
        'unit_price': [10.0, 5.0, 2.0]
    })
    out = transform(df)
    assert out.loc[0, 'quantity'] == 1
    assert out.loc[1, 'quantity'] == 1
    assert isinstance(out.loc[0, 'quantity'], (int, np.integer))
