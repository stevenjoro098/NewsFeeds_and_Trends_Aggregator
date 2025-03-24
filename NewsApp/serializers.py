from rest_framework import serializers

from .models import GDLETNewsModel

class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = GDLETNewsModel
        fields = '__all__'