from datetime import datetime
import time
import requests
from celery import shared_task
from pytz import timezone

from NewsApp.models import GDLETNewsModel

API_URL = "https://api.gdeltproject.org/api/v2/doc/doc?query=technology&mode=artlist&format=json"  # Replace with your actual GDELT API

@shared_task
def collect_news():
    url = "https://api.gdeltproject.org/api/v2/doc/doc?query=technology&format=json"
    gdelt_api = "https://api.gdeltproject.org/api/v2/doc/doc?query=global+news&mode=artlist&format=json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(gdelt_api, headers=headers)
    if response.status_code == 200:
        data = response.json().get('articles', [])  # Extract articles list
        for article in data:
            # Ensure no duplicate entries
            if not GDLETNewsModel.objects.filter(url=article.get('url')).exists():
                GDLETNewsModel.objects.create(
                    title=article.get('title', 'No Title'),
                    url=article.get('url'),
                    content=article.get('content', ''),
                    summary=None,  # Summary will be processed later
                    domain=article.get('domain', ''),
                    language=article.get('language', ''),
                    published_at=datetime.strptime(article.get('seendate', ''), '%Y-%m-%dT%H:%M:%SZ') if article.get(
                        'seendate') else None
                )
        return f"Fetched {len(data)} new articles"
    return "Failed to fetch news"