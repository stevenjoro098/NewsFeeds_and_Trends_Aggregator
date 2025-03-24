import os
from celery import Celery
from nltk.inference.resolution import Clause

os.environ.setdefault('DJANGO_SETTINGS_MODULE','NewsFeed.settings')

app = Celery('NewsFeed')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()