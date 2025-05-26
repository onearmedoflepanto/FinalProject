from django.db import models
from django.conf import settings

# Create your models here.

class StockDetail(models.Model):
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_stocks', blank=True)    
    name = models.TextField(unique=True)
    code = models.TextField()
    price = models.IntegerField()
    change = models.FloatField()
    chart = models.ImageField(upload_to="stocks/charts/", null=True, blank=True)

class StockComments(models.Model):
    stock = models.ForeignKey(StockDetail, on_delete=models.CASCADE)
    content = models.CharField(max_length = 20)