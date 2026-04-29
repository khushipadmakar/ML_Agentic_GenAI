import pandas as pd


def load_data(file):
    """
    Load CSV or JSON data (supports file path + Streamlit upload)
    """

    # Case 1: Streamlit UploadedFile
    if hasattr(file, "name"):
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        elif file.name.endswith(".json"):
            return pd.read_json(file)
        else:
            raise ValueError("Unsupported file format")

    # Case 2: File path string
    elif isinstance(file, str):
        if file.endswith(".csv"):
            return pd.read_csv(file)
        elif file.endswith(".json"):
            return pd.read_json(file)
        else:
            raise ValueError("Unsupported file format")

    else:
        raise ValueError("Invalid file input")


def preprocess_data(df):
    df = df.copy()

    # Convert dates
    df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True, errors='coerce')
    df['signup_date'] = pd.to_datetime(df['signup_date'], dayfirst=True, errors='coerce')
    df['review_date'] = pd.to_datetime(df['review_date'], dayfirst=True, errors='coerce')

    # Feature engineering
    df['total_amount'] = df['quantity'] * df['unit_price']

    return df