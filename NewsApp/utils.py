from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from celery import shared_task
from transformers import pipeline

nltk.download('vader_lexicon')

def SentimentAnalysis(news_title):
    # categorize news as positive, negative, or neutral.
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(news_title)
    #print(sentiment_score)  # {'neg': 0.0, 'neu': 0.5, 'pos': 0.5, 'compound': 0.6}
    return sentiment_score


summarizer = pipeline("summarization")

@shared_task
def process_gdelt_news():
    unprocessed_news = GDELTNews.objects.filter(summary__isnull=True)  # Only process new data
    for news in unprocessed_news:
        news.summary = summarizer(news.content, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
        news.save()