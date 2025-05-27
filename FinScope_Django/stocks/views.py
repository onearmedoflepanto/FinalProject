from .static.get_stock_graph import get_stock_graph, stock_code_search

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
import html
import re
from decouple import config

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
        "X-Naver-Client-Id": config("NAVER_API_ID"),
        "X-Naver-Client-Secret": config("NAVER_API_SECRET"),
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


@api_view(["GET"])
def get_exchange_info(request):
    try:
        exchange_usd = requests.get(
            "https://m.search.naver.com/p/csearch/content/qapirender.nhn?key=calculator&pkid=141&q=%ED%99%98%EC%9C%A8&where=m&u1=keb&u6=standardUnit&u7=0&u3=USD&u4=KRW&u8=down&u2=1"
        ).json()
        exchange_jpy = requests.get(
            "https://m.search.naver.com/p/csearch/content/qapirender.nhn?key=calculator&pkid=141&q=%ED%99%98%EC%9C%A8&where=m&u1=keb&u6=standardUnit&u7=0&u3=JPY&u4=KRW&u8=down&u2=1"
        ).json()
        exchange_cny = requests.get(
            "https://m.search.naver.com/p/csearch/content/qapirender.nhn?key=calculator&pkid=141&q=%ED%99%98%EC%9C%A8&where=m&u1=keb&u6=standardUnit&u7=0&u3=CNY&u4=KRW&u8=down&u2=1"
        ).json()

        exchange_usd = float(exchange_usd["country"][1]["value"].replace(",", ""))
        exchange_jpy = float(exchange_jpy["country"][1]["value"].replace(",", "")) * 100
        exchange_cny = float(exchange_cny["country"][1]["value"].replace(",", "")) * 10

        data = {"USD": exchange_usd, "JPY": exchange_jpy, "CNY": exchange_cny}
    except Exception as e:
        print("환율 조회 api 오류.", e)
        data = {"USD": 1000, "JPY": 2000, "CNY": 1000}

    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_news_list(request):
    url = "https://openapi.naver.com/v1/search/news.json"
    params = {"query": "주식", "display": 5, "sort": "date"}
    headers = {
        "X-Naver-Client-Id": config("NAVER_API_ID"),
        "X-Naver-Client-Secret": config("NAVER_API_SECRET"),
    }
    res = requests.get(url, params=params, headers=headers)
    data = []
    for news in res.json().get("items", []):
        title = html.unescape(news["title"])
        processed = re.sub(r"<[^>]+>", "", title)
        description = html.unescape(news["description"])
        processed_description = re.sub(r"<[^>]+>", "", description)
        data.append(
            {
                "title": processed,
                "link": news["link"],
                "description": processed_description,
            }
        )

    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_chart_graph(request, name):
    data = get_stock_graph(name)

    if data is None:
        return Response(
            {"error": "차트 데이터 조회 실패"}, status=status.HTTP_400_BAD_REQUEST
        )
    else:
        return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_chart_code(request, name):
    code = stock_code_search(name)
    return Response({"code": code}, status=status.HTTP_200_OK)
