from django.db import models
from django.contrib.auth import get_user_model
from stocks.models import StockDetail

# Create your models here.

class Comment(models.Model):
    stock = models.ForeignKey(StockDetail, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)