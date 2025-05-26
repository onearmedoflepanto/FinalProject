import requests
import json
import re
import time
from pathlib import Path
from decouple import config
import os
import json
import datetime
import pandas as pd

APP_KEY = config("KIS_API_ID")
APP_SECRET = config("KIS_API_SECRET")

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


def stock_code_search(name):
    url = "https://m.stock.naver.com/front-api/search/autoComplete"
    params = {"query": name, "target": "stock,index,marketindicator,coin,ipo"}
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

    response = requests.get(url, params=params, headers=headers)
    return response.json()


def decrease_time(time_str, minutes):
    """time_str을 분 단위로 감소시켜서 새로운 시간을 반환"""
    time_format = "%H%M%S"
    dt = datetime.datetime.strptime(time_str, time_format)
    dt -= datetime.timedelta(minutes=minutes)
    return dt.strftime(time_format)


def get_domestic_stock_info(access_token, stock_code):
    time_end = "153000"
    PATH = "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice"
    URL = f"{BASE_URL}{PATH}"

    all_data = []

    while True:

        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {access_token}",
            "appKey": APP_KEY,
            "appSecret": APP_SECRET,
            "tr_id": "FHKST03010200",
        }

        params = {
            "FID_ETC_CLS_CODE": "",  # 기타 구분 코드
            "FID_COND_MRKT_DIV_CODE": "J",  # 시장 분류 코드
            "FID_INPUT_ISCD": stock_code,  # 종목 코드
            "FID_INPUT_HOUR_1": time_end,  # 조회 종료 시간 (HHMMSS)
            "FID_PW_DATA_INCU_YN": "N",  # 과거 데이터 포함 여부 (N: 당일만 조회)
        }

        res = requests.get(URL, headers=headers, params=params)
        if res.status_code == 200:
            res_data = res.json()
            data = res_data.get("output2", [])
            if data:
                # OHLCV 데이터를 DataFrame으로 변환
                ohlcv_data = [
                    {
                        "Date": item["stck_bsop_date"],  # 거래일자
                        "Time": item["stck_cntg_hour"],  # 체결 시간
                        "Open": item["stck_oprc"],  # 시가
                        "High": item["stck_hgpr"],  # 고가
                        "Low": item["stck_lwpr"],  # 저가
                        "Close": item["stck_prpr"],  # 종가
                        "Volume": item["cntg_vol"],  # 체결 거래량
                    }
                    for item in data
                ]

                all_data.extend(ohlcv_data)

                # 30개의 데이터를 받았으면 time_end를 줄여서 다음 데이터를 요청
                time_end = decrease_time(time_end, minutes=30)
            else:
                print("No more data available for the specified time.")
                break
        else:
            print(f"Failed to retrieve data: {res.status_code}, {res.text}")
            break

    # DataFrame 생성 및 정렬
    df = pd.DataFrame(all_data)
    df["DateTime"] = pd.to_datetime(
        df["Date"] + df["Time"], format="%Y%m%d%H%M%S"
    )  # 날짜와 시간 결합
    df = df.astype(
        {
            "Open": "float",
            "High": "float",
            "Low": "float",
            "Close": "float",
            "Volume": "float",
        }
    )  # 데이터 타입 변환
    df = df[["DateTime", "Open", "High", "Low", "Close", "Volume"]]
    df = df.sort_values(by="DateTime", ascending=True)
    df = df.reset_index(drop=True)

    return df


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
        return data
    else:
        print("데이터 오류:", response.status_code, response.text)


def get_stock_graph(name):
    company_name = name
    jsondata = stock_code_search(company_name)

    try:
        item = jsondata["result"]["items"][0]
        stock_code = item["code"]
        print(f"[검색된 종목 코드]: {stock_code}")
    except (KeyError, IndexError):
        print("데이터 수신 오류")
        return None

    access_token = load_cached_token()
    if not access_token:
        access_token = get_access_token()

    if re.fullmatch(r"\d+", stock_code):
        return get_domestic_stock_info(access_token, stock_code)
    elif re.fullmatch(r"[A-Z.]+", stock_code):
        return get_overseas_stock_info(access_token, stock_code)
    else:
        print("코드 입력 오류/", stock_code)
        return None
