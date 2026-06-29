# Stock Sentiment Analyzer 🚀

A web app that performs analysis on real-time stock news to determine whether a stock is Bullish, Neutral, or Bearish, helping investors make informed decisions.

## 📌 Overview

This project pulls real time stock news using NewsAPI, forms a valuable sentiment using the SentimentIntensityAnalyzer and gives the user whether the market is Bullish, Neutral, or Bearish on that stock

## Live demo

[Stock Sentiment Analyzer](https://stock-sentiment-analyzer-x41c.onrender.com/)

## Features

- Real-time news sentiment analysis for any stock ticker
- Classifies sentiment as 🟢 Bullish, 🟡 Neutral, or 🔴 Bearish
- Displays latest news headlines with individual sentiment scores
- Clickable headlines linking to full articles

## How it Works

1. User enters a stock ticker (e.g. AAPL, TSLA)
2. App fetches latest news from NewsAPI
3. VADER sentiment analysis runs on each headline
4. Average compound score determines overall market sentiment
5. Results displayed with emoji indicators

## Limitations

- VADER lacks financial context (e.g. "rate cuts" may be misclassified)
- NewsAPI free tier limited to 100 requests/day
- Stock price chart temporarily removed due to API constraints

## Future Improvements

- Upgrade to FinBERT for finance-aware sentiment analysis
- Add stock price chart using a reliable financial data API
- Add caching to reduce API calls

## How to Run Locally

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your API keys to a `.env` file:
4. Run: `streamlit run streamlit_app.py`
