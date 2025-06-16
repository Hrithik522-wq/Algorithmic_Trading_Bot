import requests
import os
from dotenv import load_dotenv
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fundamental_analysis():
    try:
        url = f"https://newsapi.org/v2/everything?q=ECB+interest+rate&apiKey={NEWS_API_KEY}&pageSize=3"
        response = requests.get(url)
        articles = response.json().get("articles", [])
        headlines = " ".join([a["title"] for a in articles])
        sentiment = "positive" if any(keyword in headlines.lower() for keyword in ["cut", "support", "boost", "stability"]) else "negative"
        print(f"Fundamental Analysis (Real News): {headlines} => Sentiment: {sentiment}")
        return sentiment
    except Exception as e:
        print(f"Fundamental API error: {e}")
        return "neutral"
