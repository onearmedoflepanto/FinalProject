from .static.get_stock_graph import get_stock_graph, stock_code_search
from .static.get_recommend import get_recommend

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
import json
from decouple import config
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# Create your views here.


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def my_favorites(request):
#     stocks = request.user.favorite_stocks.all()
#     serializer = StockSerializer(stocks, many=True)
#     return Response(serializer.data)


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
    query = request.GET.get("q", "주식")
    print(f"쿼리 : {query}")

    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": config("NAVER_API_ID"),
        "X-Naver-Client-Secret": config("NAVER_API_SECRET"),
    }
    params = {"query": query, "display": 10, "start": 1, "sort": "date"}

    res = requests.get(url, headers=headers, params=params)
    cleaned_data = []

    for news in res.json().get("items", []):
        title = html.unescape(news["title"])
        title = re.sub(r"<[^>]*>", "", title)

        description = html.unescape(news["description"])
        description = re.sub(r"<[^>]*>", "", description)

        cleaned_data.append(
            {
                "title": title.strip(),
                "link": news["link"],
                "description": description.strip(),
            }
        )

    return JsonResponse({"items": cleaned_data})


# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def toggle_favorite(request, name):
#     print(f"toggle_favorite called with name: {name} (type: {type(name)})")
#     try:
#         stock, created = StockDetail.objects.get_or_create(name=name)
#         if created:
#             print(f"Created new StockDetail for: {name}")
#         else:
#             print(f"Found existing StockDetail for: {name}, pk: {stock.pk}")
        
#         user = request.user
#         print(f"User: {user.username} (pk: {user.pk})")

#         # Explicitly check if stock object is valid before M2M access
#         if not stock or not hasattr(stock, 'favorites'):
#             print(f"Error: Stock object for '{name}' is invalid or missing 'favorites' manager.")
#             return Response({"error": "Invalid stock data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         is_currently_favorite = stock.favorites.filter(pk=user.pk).exists()
#         print(f"Is '{name}' favorite for '{user.username}'? {is_currently_favorite}")

#         if request.method == "GET":
#             return Response({"favorites": is_currently_favorite}, status=status.HTTP_200_OK)

#         elif request.method == "POST":
#             if is_currently_favorite:
#                 stock.favorites.remove(user)
#                 message = "즐겨찾기에서 제거되었습니다."
#                 new_favorite_status = False
#                 print(f"Removed '{name}' from favorites for '{user.username}'")
#             else:
#                 stock.favorites.add(user)
#                 message = "즐겨찾기에 추가되었습니다."
#                 new_favorite_status = True
#                 print(f"Added '{name}' to favorites for '{user.username}'")
            
#             return Response({"message": message, "is_favorite": new_favorite_status}, status=status.HTTP_200_OK)

#     except Exception as e:
#         print(f"!!! Exception in toggle_favorite for name '{name}': {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return Response({"error": f"Server error processing favorite toggle: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    params = {"query": "주식", "display": 15, "sort": "date"} # Increased display from 5 to 15
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
    period = request.GET.get('period', '1d') # Default to '1d' (intraday) if not provided
    data = get_stock_graph(name, period=period) # Pass period to the function

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


@api_view(["GET"])
def get_ai_recommend(request):
    user_info_str = request.GET.get("user_info")
    try:
        user_info = (
            json.loads(user_info_str) if user_info_str else {"tendency": "normal"}
        )
    except json.JSONDecodeError:
        user_info = {"tendency": "normal"}

    response_text = get_recommend(user_info)
    print(repr(response_text))

    try:
        result = json.loads(response_text)
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        print("문자열 처리 실패:", e)
        fallback = [{"name": "데이터 로드 오류", "type": "deposit"}]
        return Response(fallback, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def get_video_summary(request, video_id):
    try:
        GEMINI_API_KEY = config("GEMMINI_API_KEY") # Note: GEMMINI typo from .env
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash-latest') # Or other suitable model

        # Get transcript
        try:
            # Using get_transcript directly might be more straightforward
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
            
            transcript_text = " ".join([item['text'] for item in transcript_data])
            if not transcript_text.strip():
                return Response({"error": "Empty transcript found."}, status=status.HTTP_404_NOT_FOUND)

        except TranscriptsDisabled:
            return Response({"error": "Transcripts are disabled for this video."}, status=status.HTTP_400_BAD_REQUEST)
        except NoTranscriptFound:
            return Response({"error": "No Korean or English transcript found for this video."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error fetching transcript for {video_id}: {e}")
            return Response({"error": f"Could not fetch transcript: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Summarize with Gemini
        # Adjust prompt as needed
        prompt = f"다음 유튜브 영상 스크립트를 한국어로 요약해줘. 주요 내용과 핵심만 간결하게 요약해줘:\n\n{transcript_text[:10000]}" # Limit transcript length if necessary
        
        response = model.generate_content(prompt)
        summary = response.text

        return Response({"summary": summary}, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"Error generating video summary for {video_id}: {e}")
        return Response({"error": f"Failed to generate summary: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
