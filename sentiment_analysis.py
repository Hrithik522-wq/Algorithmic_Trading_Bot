import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def sentiment_analysis():
    try:
        url = f"https://newsapi.org/v2/top-headlines?q=EURUSD&apiKey={NEWS_API_KEY}&pageSize=5"
        response = requests.get(url)
        articles = response.json().get("articles", [])
        headlines = " ".join([a["title"] for a in articles])
        positive_keywords = ["rise", "bull", "gain", "strong"]
        negative_keywords = ["fall", "bear", "loss", "weak"]
        score = sum(1 for word in positive_keywords if word in headlines.lower()) - sum(1 for word in negative_keywords if word in headlines.lower())
        sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"
        print(f"Sentiment Analysis (News headlines): Score={score} => {sentiment}")
        return sentiment
    except Exception as e:
        print(f"Sentiment API error: {e}")
        return "neutral"
