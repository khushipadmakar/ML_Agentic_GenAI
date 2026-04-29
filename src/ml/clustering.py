from sklearn.cluster import KMeans

def run_clustering(df):
    features = df[['quantity', 'unit_price', 'total_amount']]

    model = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = model.fit_predict(features)

    return df, model