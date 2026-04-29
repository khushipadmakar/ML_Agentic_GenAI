import pandas as pd
import json


def load_data(file_path):
    """
    Load dataset from CSV or JSON file
    """
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file_path.endswith(".json"):
        with open(file_path, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)

    else:
        raise ValueError("Unsupported file format. Use CSV or JSON.")

    return df