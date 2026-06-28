import streamlit as st  # For UI
import requests     # helps make HTTP calls from code
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

analyzer = SentimentIntensityAnalyzer()

def get_stock_data(ticker):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHA_VANTAGE_KEY}"
    response = requests.get(url)
    data = response.json()
    
    # Extract daily closing prices
    time_series = data["Time Series (Daily)"]
    dates = list(time_series.keys())[:30]  # last 30 days
    closes = [float(time_series[date]["4. close"]) for date in dates]
    
    return dates, closes

def get_news(ticker):
    # NewsAPI has this format for URL
    url = f"https://newsapi.org/v2/everything?q={ticker}+stock+market&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"

    # gets every news regarding the searched Ticker
    response = requests.get(url)

    # Gets the most recent 10 articles on ticker
    articles = response.json()["articles"][:10]
    return [{"title": article["title"], "url": article["url"]} for article in articles]   ## Only returning the headline for sentiment analysis

def get_sentiment(articles):
    
    score = 0
    for title in articles:
        score += analyzer.polarity_scores(title["title"])["compound"]
    
    score = score/len(articles)
    return score

st.title("📈 Stock Sentiment Analyzer")
st.write("Enter a stock ticker to see price trends and news sentiment.")

ticker = st.text_input("Stock Ticker (e.g. AAPL, TSLA, NVDA)").upper()

try:
    if st.button("Search"):
        with st.spinner("Fetching data..."):
    
            dates, closes = get_stock_data(ticker)
            articles = get_news(ticker)
            sentiment_score = get_sentiment(articles)


            if sentiment_score > 0.05:
                st.subheader(f"{ticker} - Last 30 days 🟢 Bullish")
            elif 0.05 >= sentiment_score >= -0.05:
                st.subheader(f"{ticker} - Last 30 days 🟡 Neutral")

            elif sentiment_score < -0.05:
                st.subheader(f"{ticker} - Last 30 days 🔴 Bearish")

            st.line_chart({"Close": closes})

            
            st.write(f"Sentiment Score: {round(sentiment_score, 2)}")

            st.subheader("Latest News")
            for article in articles:
                score = analyzer.polarity_scores(article["title"])["compound"]
                if score > 0.05:
                    emoji = "🟢"
                elif score < -0.05:
                    emoji = "🔴"
                else:
                    emoji = "🟡"
                st.write(f"{emoji} [{article['title']}]({article['url']})")

except KeyError:
    st.error("Invalid ticker. Please try again.")

