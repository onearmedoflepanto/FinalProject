from django.urls import path
from . import views


urlpatterns = [
    # path("hot/", views.hot),
    path("favorites/", views.my_favorites),
    path("detail/<str:name>/", views.detail),
    path("<str:name>/favorite/", views.toggle_favorite),
    path("commodities-summary/", views.get_commodity_prices),
    path("get_news/", views.get_news),
    path("get_news/", views.get_news),
    path("exchange-summary/", views.get_exchange_info),
    path("news-list/", views.get_news_list),
    path("stock-chart/<str:name>/", views.get_chart_graph),
    path("chart-code/<str:name>/", views.get_chart_code),
]
