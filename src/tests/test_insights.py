import pandas as pd
from src.insights.generator import generate_insights


def test_generate_insights():

    df = pd.DataFrame({
        "cluster": [0, 1, 1],
        "total_amount": [100, 500, 600],
        "anomaly": [0, 1, 0]
    })

    daily_trend = pd.DataFrame({
        "spike": [False, True],
        "pct_change": [0.05, 0.40]
    })

    weekly_trend = pd.DataFrame({
        "weekly_pct_change": [0.10, 0.25]
    })

    insights = generate_insights(
        df,
        daily_trend,
        weekly_trend
    )

    assert len(insights) > 0
    assert insights[0].type == "cluster"