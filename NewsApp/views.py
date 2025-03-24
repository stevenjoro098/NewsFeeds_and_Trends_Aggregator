import json

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import NewsSerializers
from .models import GDLETNewsModel


# Create your views here.
class ListNews(APIView):
    def get(self, *args, **kwargs):
        try:
            news_feeds_data = GDLETNewsModel.objects.all()
            serialized_data = NewsSerializers(news_feeds_data, many=True).data

            return Response({'response': serialized_data}, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)