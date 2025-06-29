import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as ply
from datetime import datetime, timedelta

st.title('Market Sentiment Tracker')

#tickers and date
end_date = datetime.today()
start_date = end_date - timedelta(days = 40)

@st.cache_data
def load_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

df = pd.read_csv("sentiment_summary.csv")


for x in range(7):
    with st.expander(df.iloc[x,0]):
        #News outlook from CSV
        col1, col2, col3 = st.columns(3)
        col1.metric("Last 24 Hours:", df.iloc[x,1])
        col2.metric("Last 7 Days:", df.iloc[x,2])
        col3.metric("Last 30 Days:", df.iloc[x,3])

        #Actual Stock values
        ticker = df.iloc[x,0]

        data = load_data(ticker, start_date, end_date)

        if len(data) < 25:
            st.warning("Not enough trading data to show full 30-day analysis.")
        else:
            # Keep only the last 30 trading days
            data = data.tail(30)

            # Prices for change calculation
            price_today = data["Close"].iloc[-1]
            price_1d = data["Close"].iloc[-2]
            price_7d = data["Close"].iloc[-8]
            price_30d = data["Close"].iloc[0]

            # Changes
            change_1d = price_today - price_1d
            change_7d = price_today - price_7d
            change_30d = price_today - price_30d

            pct_1d = (change_1d / price_1d) * 100
            pct_7d = (change_7d / price_7d) * 100
            pct_30d = (change_30d / price_30d) * 100

            # Show metrics
            price = "%.2f" % price_today
            st.subheader("Stock Prices")
            st.caption(price)
            
            change_1dformated = "%.2f" % change_1d
            change_7dformated = "%.2f" % change_7d
            change_30dformated = "%.2f" % change_30d

            price_1dformated = "%.2f" % price_1d
            price_7dformated = "%.2f" % price_7d
            price_30dformated = "%.2f" % price_30d


            col4, col5, col6 = st.columns(3)
            col4.metric("1 Day", price_1dformated, change_1dformated)
            col5.metric("7 Days", price_7dformated, change_7dformated)
            col6.metric("30 Days", price_30dformated, change_30dformated)
            

            # Plot chart
            st.subheader("Last 30 Trading Days")
            fig, ax = ply.subplots()
            ax.plot(data.index, data["Close"], marker="o", linestyle="-", color="green")
            ax.set_xlabel("Date")
            ax.set_ylabel("Closing Price (USD)")
            ax.grid(True)
            st.pyplot(fig)
