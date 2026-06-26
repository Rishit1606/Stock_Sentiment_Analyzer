import streamlit as st
import yfinance as yf
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os

st.title("📈 Stock Sentiment Analyzer")
st.write("Enter a stock ticker to see price trends and news sentiment.")

ticker = st.text_input("Stock Ticker (e.g. AAPL, TSLA, NVDA)")

if st.button("Search"):
    st.write(f"Searching for {ticker}...")

    stock = yf.Ticker(ticker)
    history = stock.history(period="1mo")

    st.subheader(f"{ticker} - Last 30 days")
    st.line_chart(history["Close"])
