import streamlit as st  # For UI
import requests     # helps make HTTP calls from code
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os
load_dotenv()


NEWS_API_KEY = os.getenv("NEWS_API_KEY")

analyzer = SentimentIntensityAnalyzer()


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
            
            articles = get_news(ticker)
            sentiment_score = get_sentiment(articles)


            if sentiment_score > 0.05:
                st.subheader(f"{ticker} - Last 30 days 🟢 Bullish")
            elif 0.05 >= sentiment_score >= -0.05:
                st.subheader(f"{ticker} - Last 30 days 🟡 Neutral")

            elif sentiment_score < -0.05:
                st.subheader(f"{ticker} - Last 30 days 🔴 Bearish")

            
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

