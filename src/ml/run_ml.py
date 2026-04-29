from ml.clustering import run_clustering
from ml.anomaly import detect_anomalies
from ml.trends import compute_trends
from utils.preprocessing import load_data, preprocess_data


def run_ml_pipeline(file_path):
    # Load
    df = load_data(file_path)

    # Preprocess
    df = preprocess_data(df)

    # ML
    df, _ = run_clustering(df)
    df, _ = detect_anomalies(df)

    # Trends (returns TWO values)
    daily_trend, weekly_trend = compute_trends(df)

    return df, daily_trend, weekly_trend


if __name__ == "__main__":
    df, daily, weekly = run_ml_pipeline("data/sample_data.csv")

    print("\nProcessed Data:")
    print(df.head())

    print("\nDaily Trends:")
    print(daily.head())

    print("\nWeekly Trends:")
    print(weekly.head())