import requests
import json
import re
import time
from pathlib import Path
from datetime import date

APP_KEY = "PS4M8p4kbX9mVmlPW1eCl2DeNo7uoMeAUuWf"
APP_SECRET = "7EU0okINfd9YJnLyAqfJNpxE+dr+uwQGgJ+6Fey5AHKUQDWzCqnB1Pd2B3roV/G8jDBDwAl16GNCmnRd26SHTeqPeT9Ofd8BO/UPgGgpnGp79t39kRmbWQCNVJhX8V5RxYUEF+zecX6nc1nAdAGmJuxyc49V0ccHX3Q1NRvXSS11uuyGr2A="

BASE_URL = "https://openapi.koreainvestment.com:9443"
TOKEN_FILE = Path("accestoken.json")


def get_access_token():
    url = f"{BASE_URL}/oauth2/tokenP"
    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        token = response.json()["access_token"]
        expires = int(time.time()) + 3600

        with open(TOKEN_FILE, "w") as f:
            json.dump({"token": token, "expires": expires}, f)
            print(f"토큰 저장 성공 | token: {token}, 만료 시간: {expires}")
        return token
    else:
        raise Exception(f"토큰 요청 실패: {response.status_code} {response.text}")


def load_cached_token():
    if not TOKEN_FILE.exists():
        return None
    try:
        with open(TOKEN_FILE, "r") as f:
            data = json.load(f)
            if data["expires"] > int(time.time()) + 5:
                return data["token"]
    except Exception as e:
        print(f"토큰 파일 읽기 실패: {e}")
    return None


def stockcodesearch(name):
    url = "https://m.stock.naver.com/front-api/search/autoComplete"
    params = {"query": name, "target": "stock,index,marketindicator,coin,ipo"}
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

    response = requests.get(url, params=params, headers=headers)
    return response.json()


def get_domestic_stock_info(access_token, stock_code):
    url = f"{BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn"
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {access_token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHKST03010200",
        "tr_count": "",
        "custtype": "P",
        "hashkey": access_token,
    }
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": stock_code,
        "FID_INPUT_HOUR_1": "090000",
        "FID_PW_DATA_INCU_YN": "",
        "FID_ETC_CLS_CODE": "",
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print("조회 실패:", response.status_code, response.text)


def get_overseas_stock_info(access_token, stock_code):
    url = f"{BASE_URL}/uapi/overseas-price/v1/quotations/dailyprice"
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {access_token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "HHDFS76240000",
    }
    params = {
        "AUTH": "",
        "EXCD": "NAS",
        "SYMB": stock_code,
        "GUBN": 0,
        "BYMD": "",
        "MODP": 0,
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print("데이터 오류:", response.status_code, response.text)


def get_stock_graph(name):
    company_name = name
    jsondata = stockcodesearch(company_name)

    try:
        item = jsondata["result"]["items"][0]
        stock_code = item["code"]
        print(f"[검색된 종목 코드]: {stock_code}")
    except (KeyError, IndexError):
        print("데이터 수신 오류")
        return

    access_token = load_cached_token()
    if not access_token:
        access_token = get_access_token()

    if re.fullmatch(r"\d+", stock_code):
        get_domestic_stock_info(access_token, stock_code)
    elif re.fullmatch(r"[A-Z.]+", stock_code):
        get_overseas_stock_info(access_token, stock_code)
    else:
        print("코드 입력 오류/", stock_code)
