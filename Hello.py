import streamlit as st

try:
    st.set_page_config(
        page_title="Overview",
        page_icon="💵",
    )

    st.write("# Welcome to our financial portal!")

    st.sidebar.success("Select a page above.")

    st.markdown(
        """
        With this portal we aim to make your financial life a breeze!
        Investing can be intimidating, with over 6000 stocks listed on
        NYSE alone. That's where we come in! Our portal allows you to 
        ealisy navigate historical prices, understand market fluctuations
        and generate theoretical P&L analysis for different timeframes.

        ### Want to dive even deeper?

        On top of this, you have access to our very own algorithmic trading
        tool, that will tell you wether to buy, sell or hold a stock depending
        on the latest information available on the market.

        **👈 Select a page from the sidebar** to see some examples
        of how our portal works!

        We hope you have fun! If you have any concerns or doubts, please feel
        free to contact us at fin_tool@gmail.com


        This tool was created by a team composed of Pablo Gallegos, CFA; Isaac
        Chaljub, Maine Isasi, Margarida Pereira, and Sanjo Joy. We integrate
        knwoledge from different areas, which pushed us to consider how we could
        make it as good as possible for the everyday user.

    """
    )
except Exception as e:
            print(f'Error setting the Hello page:{e}')