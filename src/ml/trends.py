import pandas as pd
import numpy as np


def compute_trends(df):
    df = df.copy()

    # Convert date correctly
    df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True)

    # Sort
    df = df.sort_values('order_date')

    # Create total_amount if not exists
    if 'total_amount' not in df.columns:
        df['total_amount'] = df['quantity'] * df['unit_price']

    # -------------------------------
    # DAILY SALES (Time Series)
    # -------------------------------
    daily = df.groupby('order_date')['total_amount'].sum().reset_index()

    # Fill missing dates (important for time series)
    full_range = pd.date_range(start=daily['order_date'].min(),
                               end=daily['order_date'].max())

    daily = daily.set_index('order_date').reindex(full_range).fillna(0)
    daily.index.name = 'order_date'
    daily = daily.reset_index()

    # -------------------------------
    # Rolling Mean (smaller window for small data)
    # -------------------------------
    daily['rolling_mean_3'] = daily['total_amount'].rolling(window=3, min_periods=1).mean()

    # -------------------------------
    # Percent Change
    # -------------------------------
    daily['pct_change'] = daily['total_amount'].pct_change().fillna(0)

    # -------------------------------
    # Z-score (handle small data safely)
    # -------------------------------
    mean = daily['total_amount'].mean()
    std = daily['total_amount'].std()

    if std == 0:
        std = 1

    daily['z_score'] = (daily['total_amount'] - mean) / std

    # -------------------------------
    # Spike / Drop Detection
    # -------------------------------
    daily['spike'] = daily['pct_change'] > 0.5
    daily['drop'] = daily['pct_change'] < -0.5

    # -------------------------------
    # Weekly Trend (still works even with small data)
    # -------------------------------
    weekly = df.resample('W', on='order_date')['total_amount'].sum().reset_index()
    weekly['weekly_pct_change'] = weekly['total_amount'].pct_change().fillna(0)

    return daily, weekly