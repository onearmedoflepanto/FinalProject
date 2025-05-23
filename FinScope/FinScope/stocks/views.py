from .static.get_stock_graph import get_stock_graph

from .models import StockDetail
from .serializers import StockSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import yfinance as yf
import requests

# Create your views here.


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_favorites(request):
    stocks = request.user.favorite_stocks.all()
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def detail(request, name):
    try:
        res = get_stock_graph(name)
        return Response(res, status=status.HTTP_200_OK)
    except:
        return Response(
            {"message": "API 조회 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_news(request):
    query = request.GET.get("query", "삼성전자")

    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": "b0M_QXN6Gq2OJQNRMQxV",
        "X-Naver-Client-Secret": "MMSZgyrptA",
    }
    params = {"query": query, "display": 10, "start": 1, "sort": "date"}

    res = requests.get(url, headers=headers, params=params)
    return JsonResponse(res.json())


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, name):
    stock = get_object_or_404(StockDetail, name=name)
    user = request.user

    if request.method == "GET":
        if user in stock.favorites.all():
            return Response({"favorites": True}, status=status.HTTP_200_OK)
        else:
            return Response({"favorites": False}, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if user in stock.favorites.all():
            stock.favorites.remove(user)
            return Response({"message": "즐겨찾기 취소"}, status=200)
        else:
            stock.favorites.add(user)
            return Response({"message": "즐겨찾기 추가"}, status=201)


@api_view(["GET"])
def get_commodity_prices(request):
    tickers = {"gold": "GC=F", "silver": "SI=F", "oil": "CL=F"}
    mode = request.GET.get("mode", "latest").lower()

    data = {}
    for name, symbol in tickers.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d", interval="60m")
            if hist.empty:
                raise Exception("No data available")

            if mode == "full":
                price_data = hist["Close"].round(2).dropna()
                data[name] = {str(k): float(v) for k, v in price_data.items()}
            else:
                last_price = hist["Close"].dropna().iloc[-1]
                data[name] = float(round(last_price, 2))
        except Exception as e:
            data[name] = {"error": str(e)}
    return Response(data, status=status.HTTP_200_OK)
