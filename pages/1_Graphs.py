import polars as pl
import streamlit as st
import plotly.express as px


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from financial_data import FinancialData


###########################################################
st.set_page_config(layout='wide', page_title="Historical financial data", page_icon="📈")

#st.markdown("# Plotting Page")
st.sidebar.header("Plotting Page")


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


@st.cache_data()
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





# @st.cache_data
def plot_stock_data():
    try:
        comps = st.sidebar.selectbox("Select Company", COM['Company Name'].to_list())
        tk=COM.filter(pl.col('Company Name')==comps)['Ticker'].to_list()
        #Pri=PRI.with_columns(pl.col('Date').str.to_datetime('%Y-%m-%d').cast(pl.Date))

        start= st.sidebar.date_input(label='start date',value=PRI.filter(pl.col('Ticker').is_in(tk))['Date'].min(), key='start_date')
        #start= st.sidebar.time_input(label='start date',value=None)

        end= st.sidebar.date_input(label='start date',value=PRI.filter(pl.col('Ticker').is_in(tk))['Date'].max(), key='end_date')
        #end= st.sidebar.time_input(label='end date',value=None)

        run_function = st.checkbox("Perform P&L analysis")

        start_str = start.strftime('%Y-%m-%d')
        end_str   = end.strftime('%Y-%m-%d')
        #DESTINATION = st.sidebar.selectbox("Select Destination", destinations)
        

        #print(tk)
        fp=FinancialData(tk,COM,PRI)
        data=fp.get_historical_data(start_str, end_str)

        ## PLOT FIGURE 1 ##
        fig1 = px.line(
            data,
            x=data.index,
            y="close",
            title=f"{tk[0]}",
            template="none",
        )

        fig1.update_xaxes(title="Date")
        fig1.update_yaxes(title="Closing Price")

        st.plotly_chart(fig1, use_container_width=True)

        if run_function:
            result=fp.get_pl_sim(start,end)
            with st.container():
                st.write(result)
    except Exception as e:
            print(f'Error while plotting stock data:{e}')



if __name__ == "__main__":
    # This is to configure some aspects of the app
    # st.set_page_config(
    #     layout="wide", page_title="Financial Market Analysis and Prediction Tool", page_icon="📈"
    # )

    # Write titles in the main frame and the side bar
    st.title("Historic Stock Prices")
    #st.sidebar.title("Select a Company")

    plot_stock_data()
