import pandas as pd

USERS_FILE = "users.csv"
METRICS_FILE = "metrics.csv"

def load_users():
    return pd.read_csv(USERS_FILE)

def save_users(df_users):
    df_users.to_csv(USERS_FILE, index=False)

def load_metrics():
    return pd.read_csv(METRICS_FILE)
