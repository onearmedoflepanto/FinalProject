from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('scrape/', views.scrape_news_view, name='scrape_news'),
]