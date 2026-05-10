import pandas as pd
import os
def load_data(file_name):
    path = os.path.join("../data/raw", file_name)
    return pd.read_csv(path)

def store_data(df, file_name):
    path = os.path.join("../data/processed", file_name)
    df.to_csv(path, index=False)

def load_prepped_data(file_name):
    path = os.path.join("../data/processed", file_name)
    return pd.read_csv(path)

def store_bi_data(df, file_name):
    path = os.path.join("../dashboard/dashboard_export", file_name)
    df.to_csv(path, index=False)
    
def load_bi_data(file_name):
    path = os.path.join("../dashboard/powerbi_export", file_name)
    return pd.read_csv(path)