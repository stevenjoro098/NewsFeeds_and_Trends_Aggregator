from datetime import datetime
import time

import nltk
import requests
from celery import shared_task
from nltk.sentiment import SentimentIntensityAnalyzer
from pytz import timezone

from NewsApp.models import GDLETNewsModel
from transformers import pipeline

API_URL = "https://api.gdeltproject.org/api/v2/doc/doc?query=technology&mode=artlist&format=json"  # Replace with your actual GDELT API
gdelt_api = "https://api.gdeltproject.org/api/v2/doc/doc?query=global+news&mode=artlist&format=json"
url = "https://api.gdeltproject.org/api/v2/doc/doc?query=technology&format=json"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
         }
summarizer = pipeline("summarization")  # Summarization model
nltk.download('vader_lexicon')  # Sentiment model

sia = SentimentIntensityAnalyzer()

@shared_task
def collect_news():
    # Load AI Models
    response = requests.get(gdelt_api, headers=headers)

    if response.status_code == 200:
        data = response.json().get('articles', [])  # Extract articles list
        for article in data:
            # Ensure no duplicate entries
            parsed_time = datetime.strptime(article['seendate'], "%Y%m%dT%H%M%SZ")

            # Convert to UTC timezone-aware datetime (optional)
            parsed_time = parsed_time.replace(tzinfo=timezone("UTC"))
            if not GDLETNewsModel.objects.filter(url=article.get('url')).exists():
                content = article.get('content', '')
                summary = (
                    summarizer(content, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
                    if len(content.split()) > 50 else content
                )
                # Sentiment Analysis
                sentiment_score = sia.polarity_scores(article['title'])['compound']
                sentiment = "Positive" if sentiment_score > 0.05 else "Negative" if sentiment_score < -0.05 else "Neutral"

                GDLETNewsModel.objects.create(
                    url=article['url'],
                    title=article['title'],
                    summary=summary,
                    domain=article['domain'],
                    socialimage=article['socialimage'],
                    language=article['language'],
                    sentiment_analysis='sentiment',
                    seendate=parsed_time,
                )
        return f"Fetched {len(data)} new articles"
    return "Failed to fetch news"
    # y=1
    # for i in response.json().get('articles'):
    #     #print(i)
    #     try:
    #         parsed_time = datetime.strptime(i['seendate'], "%Y%m%dT%H%M%SZ")
    #
    #         # Convert to UTC timezone-aware datetime (optional)
    #
    #         parsed_time = parsed_time.replace(tzinfo=timezone("UTC"))
    #         GDLETNewsModel.objects.create(
    #             url=i['url'],
    #             title=i['title'],
    #             domain=i['domain'],
    #             socialimage=i['socialimage'],
    #             language=i['language'],
    #             seendate=parsed_time
    #         )
    #         time.sleep(3)
    #         print(f"{y} - {i['title']}.... added Successfully")
    #         y += 1
    #     except Exception as e:
    #         print(f'Error: {e}')