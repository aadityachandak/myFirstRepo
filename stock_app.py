import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(page_title="Stock Insights", layout="centered")

st.title("📈 Indian Stock Snapshot")
st.markdown("Enter an NSE/BSE stock symbol like `INFY.NS`, `HDFCBANK.NS`, or `RELIANCE.NS`")

# User input
symbol = st.text_input("Enter Script Symbol", value="INFY.NS")

if symbol:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="1y")

        if hist.empty:
            st.warning("No historical data found. Please check the symbol.")
        else:
            st.subheader(f"{info.get('shortName', 'Unknown')} ({symbol})")

            # Current Price & Stats
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Current Price", f"₹{info.get('currentPrice', 'N/A')}")
                st.metric("P/E Ratio", info.get("trailingPE", "N/A"))
                st.metric("52W High", f"₹{info.get('fiftyTwoWeekHigh', 'N/A')}")
            with col2:
                market_cap = round(info.get("marketCap", 0) / 1e7, 2)
                st.metric("Market Cap (₹ Cr)", f"{market_cap}")
                st.metric("52W Low", f"₹{info.get('fiftyTwoWeekLow', 'N/A')}")
                st.metric("Volume", info.get("volume", "N/A"))

            # Technical Averages
            hist['50DMA'] = hist['Close'].rolling(window=50).mean()
            hist['200DMA'] = hist['Close'].rolling(window=200).mean()

            st.subheader("📊 1-Year Price Trend")
            st.line_chart(hist[['Close', '50DMA', '200DMA']].dropna())

            # Show recent trendtable
            st.subheader("🕒 Last 5 Days Snapshot")
            st.dataframe(hist[['Open', 'High', 'Low', 'Close', 'Volume']].tail().round(2))

    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")