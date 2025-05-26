import os
import requests
import json
import datetime
import pandas as pd
from decouple import config

api_key = config("KIS_API_ID")
api_secret = config("KIS_API_SECRET")

URL_BASE = "https://openapi.koreainvestment.com:9443"


# 액세스 토큰 발급 함수
def get_access_token():
    """KIS API를 위한 액세스 토큰 발급"""
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": api_key,
        "appsecret": api_secret,
    }
    PATH = "/oauth2/tokenP"
    URL = f"{URL_BASE}{PATH}"

    res = requests.post(URL, headers=headers, data=json.dumps(body))

    if res.status_code == 200:
        access_token = res.json()["access_token"]
        return access_token
    else:
        print(f"Failed to get access token: {res.json()}")
        return None


def decrease_time(time_str, minutes):
    """time_str을 분 단위로 감소시켜서 새로운 시간을 반환"""
    time_format = "%H%M%S"
    dt = datetime.datetime.strptime(time_str, time_format)
    dt -= datetime.timedelta(minutes=minutes)
    return dt.strftime(time_format)


def get_minute_ohlcv_data(access_token, code="005930", time_end="153000"):
    """당일 분봉 OHLCV 데이터를 조회하고 DataFrame으로 반환"""
    PATH = "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice"
    URL = f"{URL_BASE}{PATH}"

    all_data = []

    while True:

        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {access_token}",
            "appKey": api_key,
            "appSecret": api_secret,
            "tr_id": "FHKST03010200",
        }

        params = {
            "FID_ETC_CLS_CODE": "",  # 기타 구분 코드
            "FID_COND_MRKT_DIV_CODE": "J",  # 시장 분류 코드
            "FID_INPUT_ISCD": code,  # 종목 코드
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
                print(f"Next time_end: {time_end}")
            else:
                print("No more data available for the specified time.")
                break
        else:
            print(f"Failed to retrieve data: {res.status_code}, {res.text}")
            return None

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


if __name__ == "__main__":
    access_token = get_access_token()
    if access_token:

        code_stock_krx = "032640"
        time_end = "153000"  # 종료 시간

        df = get_minute_ohlcv_data(access_token, code=code_stock_krx, time_end=time_end)
        if df is not None:
            print(df)
    else:
        print("Failed to get access token.")
