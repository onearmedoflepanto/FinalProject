from rest_framework import serializers
from .models import StockDetail, StockComments

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockDetail
        fields = '__all__'

class StockCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockComments
        fields = ('content',)