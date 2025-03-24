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
            parsed_time = datetime.strptime(article['seendate'], "%Y%m%dT%H%M%SZ")
            #
            # Convert to UTC timezone-aware datetime (optional)
            parsed_time = parsed_time.replace(tzinfo=timezone("UTC"))
            if not GDLETNewsModel.objects.filter(url=article.get('url')).exists():
                GDLETNewsModel.objects.create(
                    url=article['url'],
                    title=article['title'],
                    domain=article['domain'],
                    socialimage=article['socialimage'],
                    language=article['language'],
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