# # import feedparser
import time
from datetime import datetime
from pytz import timezone

import django
import requests
from django.core.management import BaseCommand

# # rss_url = "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
# #from NewsFeed.NewsApp.models import GDLETNewsModel
gdelt_api = "https://api.gdeltproject.org/api/v2/doc/doc?query=global+news&mode=artlist&format=json"
# url = 'https://api.gdeltproject.org/api/v2/doc/doc?query=site:bbc.com&format=json'
# # feed = feedparser.parse(rss_url)
# #
# # for entry in feed.entries:
# #     print(f"Title: {entry.title}")
# #     print(f"Link: {entry.link}")
# #     print("\n")
from NewsApp.models import GDLETNewsModel

def collect_news():
    url = "https://api.gdeltproject.org/api/v2/doc/doc?query=technology&format=json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(gdelt_api, headers=headers)
    y=1
    for i in response.json().get('articles'):
        #print(i)
        try:
            parsed_time = datetime.strptime(i['seendate'], "%Y%m%dT%H%M%SZ")

            # Convert to UTC timezone-aware datetime (optional)

            parsed_time = parsed_time.replace(tzinfo=timezone("UTC"))
            GDLETNewsModel.objects.create(
                url=i['url'],
                title=i['title'],
                domain=i['domain'],
                socialimage=i['socialimage'],
                language=i['language'],
                seendate=parsed_time
            )
            time.sleep(3)
            print(f"{y} - {i['title']}.... added Successfully")
            y += 1
        except Exception as e:
            print(f'Error: {e}')

class Command(BaseCommand):
    help = "Fetch news from GDELT API"

    def handle(self, *args, **kwargs):
        collect_news()