from src.insights.schema import Insight


def generate_insights(df, daily_trend, weekly_trend):
    insights = []

    # -------------------------------
    # 1. Cluster Insight
    # -------------------------------
    cluster_spend = df.groupby('cluster')['total_amount'].mean()
    top_cluster = cluster_spend.idxmax()

    insights.append(
        Insight(
            type="cluster",
            text=f"Customer segment {top_cluster} shows highest spending behavior",
            value=float(cluster_spend.max())
        )
    )

    # -------------------------------
    # 2. Anomaly Insight
    # -------------------------------
    anomaly_count = int(df['anomaly'].sum())

    insights.append(
        Insight(
            type="anomaly",
            text=f"{anomaly_count} unusual transactions detected",
            value=anomaly_count
        )
    )

    # -------------------------------
    # 3. Trend Spike (daily)
    # -------------------------------
    spikes = daily_trend[daily_trend['spike'] == True]

    if not spikes.empty:
        max_spike = spikes['pct_change'].max()

        insights.append(
            Insight(
                type="trend",
                text=f"Significant spike detected: {round(max_spike*100,2)}% increase in sales",
                value=float(max_spike)
            )
        )

    # -------------------------------
    # 4. Weekly Change
    # -------------------------------
    if len(weekly_trend) > 1:
        last_change = weekly_trend['weekly_pct_change'].iloc[-1]

        insights.append(
            Insight(
                type="trend",
                text=f"Weekly sales changed by {round(last_change*100,2)}%",
                value=float(last_change)
            )
        )

    return insights