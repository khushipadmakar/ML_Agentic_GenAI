# from sklearn.ensemble import IsolationForest


# def detect_anomalies(df):
#     features = df[['quantity', 'unit_price', 'total_amount']]

#     model = IsolationForest(contamination=0.2, random_state=42)

#     df['anomaly'] = model.fit_predict(features)

#     # Convert to 0/1
#     df['anomaly'] = df['anomaly'].map({1: 0, -1: 1})

#     return df, model

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd

def detect_anomalies(df):
    features = ['quantity', 'unit_price', 'total_amount']

    # Drop missing values safely
    data = df[features].copy()
    data = data.fillna(data.median(numeric_only=True))

    # Scale features (VERY IMPORTANT)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    # Better contamination (adjustable)
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,  # 5% anomalies (more realistic)
        random_state=42
    )

    preds = model.fit_predict(scaled_data)

    # Convert: 1 = normal, 0 = anomaly
    df['anomaly'] = (preds == -1).astype(int)

    return df, model