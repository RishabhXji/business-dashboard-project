from pathlib import Path
import pandas as pd
import os
import glob

# Resolve dataset path robustly:
# 1) If DATA_CSV_PATH env var is set, use it
# 2) Look for project-root/database/sales_data.csv (relative to this file's parents)
# 3) Look for workspace-level database/sales_data.csv (two levels up)
# 4) Fallback: search the repository for any sales_data.csv file

def _candidate_paths():
    candidates = []
    # env override
    env_path = os.getenv('DATA_CSV_PATH')
    if env_path:
        candidates.append(Path(env_path))

    # relative to this file: backend/app
    here = Path(__file__).resolve()
    # project root guesses
    candidates.append(here.parents[2] / 'database' / 'sales_data.csv')   # <project>/database/sales_data.csv
    candidates.append(here.parents[3] / 'database' / 'sales_data.csv')   # one level higher if structure differs
    candidates.append(here.parents[1] / 'database' / 'sales_data.csv')   # backend/app/../database

    # common user downloads path used previously
    user_downloads = Path.home() / 'Downloads' / 'database' / 'sales_data.csv'
    candidates.append(user_downloads)

    # Include any found by glob searching up to 4 levels
    repo_root = here
    for _ in range(4):
        repo_root = repo_root.parent
    # search for any sales_data.csv under repo_root (non-recursive depth-limited search)
    glob_paths = list(repo_root.glob('**/sales_data.csv'))
    for p in glob_paths:
        candidates.append(p)

    # make unique while preserving order
    seen = set()
    uniq = []
    for p in candidates:
        try:
            key = str(p.resolve())
        except Exception:
            key = str(p)
        if key not in seen:
            seen.add(key)
            uniq.append(Path(p))
    return uniq

def _find_dataset():
    for p in _candidate_paths():
        if p.exists():
            return p.resolve()
    return None

def load_data():
    """Loads CSV into a pandas DataFrame. Tries multiple candidate locations and provides a clear error message listing attempts."""
    data_path = _find_dataset()
    if data_path is None:
        tried = "\n".join([str(p) for p in _candidate_paths()[:10]])
        raise FileNotFoundError(
            "Dataset sales_data.csv not found. Looked in the following locations:\n" + tried +
            "\n\nPlease run the data generator (backend/app/data/generate_data.py) or set the DATA_CSV_PATH environment variable to the CSV location."
        )

    # read with parse_dates (order_date may or may not exist; let pandas infer if missing)
    try:
        df = pd.read_csv(data_path, parse_dates=['order_date'])
    except ValueError:
        # order_date column missing or parse error — read without parse_dates
        df = pd.read_csv(data_path)
    return df
