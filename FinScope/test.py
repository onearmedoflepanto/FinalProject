import requests
import html

url = "https://openapi.naver.com/v1/search/news.json"

params = {"query": "주식", "display": 5, "sort": "date"}

headers = {
    "X-Naver-Client-Id": "b0M_QXN6Gq2OJQNRMQxV",
    "X-Naver-Client-Secret": "MMSZgyrptA",
}

data = requests.get(url, params=params, headers=headers)

data = data.json()

for news in data["items"]:
    print(html.unescape(news["title"]))
