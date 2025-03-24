from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


# Create your views here.
class ListNews(APIView):
    def get(self, *args, **kwargs):
        try:
            
            return Response({'response':'Hello Django'}, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)