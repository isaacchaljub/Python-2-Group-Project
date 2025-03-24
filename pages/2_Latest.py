import polars as pl
import streamlit as st
import plotly.express as px


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from financial_data import FinancialData


###########################################################

st.set_page_config(layout='wide', page_title="Most recent financial data", page_icon="📈")

st.markdown("# Latest stock information")
st.sidebar.header("Latest stock information Page")

import requests
def download_large_file():
    url = "https://github.com/isaacchaljub/Python-2-Group-Project/releases/download/v1.0.0/us-shareprices-daily.csv"
    local_filename = "us-shareprices-daily.csv"

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(local_filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return local_filename

@st.cache_data
def init_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path_companies = os.path.join(script_dir, '..', 'us-companies.csv')
    csv_path_prices = download_large_file()

    COM=pl.read_csv(csv_path_companies, separator=';')
    PRI=pl.read_csv(csv_path_prices, separator=';')
    PRI=PRI.with_columns(pl.col('Date').str.to_datetime('%Y-%m-%d').cast(pl.Date))

    COM=COM.drop_nulls(subset=['Ticker'])

    return COM,PRI

COM, PRI=init_files()



def retrieve_stock_data():
    try:
        comps = st.sidebar.selectbox("Select Company", COM['Company Name'].to_list())
        tk=COM.filter(pl.col('Company Name')==comps)['Ticker'].to_list()

        fp=FinancialData(tk,COM,PRI)

        new_data=fp.get_new_prices()

        # Set page layout
        #st.set_page_config(page_title="Centered Text & DataFrame", layout="wide")

        # Custom CSS for centering
        st.markdown(
            """
            <style>
                .centered-text {
                    text-align: center;
                    font-size: 36px;
                    font-weight: bold;
                    color: #4CAF50;
                }
                .dataframe-container {
                    display: flex;
                    justify-content: center;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Centering using st.columns()
        #col1, col2, col3 = st.columns([1, 2, 1])  # Middle column (col2) will contain the text and DataFrame

        with st.container():
            #st.markdown('<p class="centered-text">📊 Your Data Overview</p>', unsafe_allow_html=True)
            st.dataframe(new_data, use_container_width=True)  # Displays DataFrame in a centered column
            #st.table(new_data)
    except Exception as e:
            print(f'Error while calling retrieve_stock_data:{e}')


if __name__ == "__main__":
    retrieve_stock_data()