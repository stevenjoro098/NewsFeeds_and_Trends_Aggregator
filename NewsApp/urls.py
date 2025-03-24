from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListNews.as_view(), name='news_list')
]