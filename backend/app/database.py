from pathlib import Path
import pandas as pd
import os

DATA_PATH = Path(__file__).resolve().parents[1] / '..' / 'database' / 'sales_data.csv'
# normalize
DATA_PATH = Path(os.path.abspath(os.path.join(Path(__file__).resolve().parents[2], '..', 'database', 'sales_data.csv')))

def load_data():
    # Loads CSV into a pandas DataFrame
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Run data generator in backend/app/data/generate_data.py to create it.")
    df = pd.read_csv(DATA_PATH, parse_dates=['order_date'])
    return df
