import polars as pl
import pandas as pd
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from preprocessing import bulk_preprocessing

def download_large_file():
    url = 'https://github.com/isaacchaljub/Python-2-Group-Project/releases/download/v2.0.0/us-shareprices-daily.parquet'
    local_filename = "us-shareprices-daily.parquet"

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(local_filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return local_filename


def init_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path_companies = os.path.join(script_dir, 'us-companies.csv')
    parquet_path_prices = download_large_file()

    COM=pl.read_csv(csv_path_companies, separator=';')
    PRI=pl.read_parquet(parquet_path_prices)
    PRI=PRI.with_columns(pl.col('Date').str.to_datetime('%Y-%m-%d').cast(pl.Date))

    COM=COM.drop_nulls(subset=['Ticker'])

    return COM,PRI

com,pri=init_files()

bulk_data=bulk_preprocessing(com, pri, com['Ticker'])

bulk_data.to_parquet('bulk_data.parquet', index=True)