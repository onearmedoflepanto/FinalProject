import requests
import json
import re
import time
from pathlib import Path
from decouple import config
import os
import json
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf # Import yfinance

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
    dt = datetime.strptime(time_str, time_format)
    dt -= timedelta(minutes=minutes)
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
            "FID_ETC_CLS_CODE": "",
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": stock_code,
            "FID_INPUT_HOUR_1": time_end,
            "FID_PW_DATA_INCU_YN": "N",
        }

        res = requests.get(URL, headers=headers, params=params)
        if res.status_code != 200:
            print(f"Failed to retrieve data: {res.status_code}, {res.text}")
            break

        data = res.json().get("output2", [])
        if not data:
            print("No more data available for the specified time.")
            break

        for item in data:
            dt_str = item["stck_bsop_date"] + item["stck_cntg_hour"]
            dt_obj = datetime.strptime(dt_str, "%Y%m%d%H%M%S")
            timestamp = int(dt_obj.timestamp() * 1000)

            all_data.append(
                {
                    "x": timestamp,
                    "o": float(item["stck_oprc"]),
                    "h": float(item["stck_hgpr"]),
                    "l": float(item["stck_lwpr"]),
                    "c": float(item["stck_prpr"]),
                    "v": int(item["cntg_vol"]),
                }
            )

        time_end = decrease_time(time_end, minutes=30)

    return sorted(all_data, key=lambda x: x["x"])


def get_overseas_stock_info(access_token, stock_code):
    def call_api(exchange_code, symbol_code, nmin, keyb="", next_value=""):
        PATH = "/uapi/overseas-price/v1/quotations/inquire-time-itemchartprice"
        URL = f"{BASE_URL}{PATH}"
        params = {
            "AUTH": "",
            "EXCD": exchange_code,
            "SYMB": symbol_code,
            "NMIN": str(nmin),
            "PINC": "1",
            "NEXT": next_value,
            "NREC": "120",
            "FILL": "",
            "KEYB": keyb,
        }
        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {access_token}",
            "appkey": APP_KEY,
            "appsecret": APP_SECRET,
            "tr_id": "HHDFS76950200",
            "custtype": "P",
        }
        time.sleep(0.1)
        response = requests.get(URL, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API 호출 실패: {response.status_code}, {response.text}")
            return None

    def get_next_keyb(output2, nmin):
        last = output2[-1]
        last_time = datetime.strptime(last["xymd"] + last["xhms"], "%Y%m%d%H%M%S")
        next_time = last_time - timedelta(minutes=nmin)
        return next_time.strftime("%Y%m%d%H%M%S")

    def convert_to_ohlcv_list(df):
        df = df[["datetime", "open", "high", "low", "last", "evol"]]
        df = df.rename(
            columns={"open": "o", "high": "h", "low": "l", "last": "c", "evol": "v"}
        )
        df["x"] = (df["datetime"].astype(int) / 10**6).astype(int)
        return df[["x", "o", "h", "l", "c", "v"]].to_dict("records")

    def convert_to_dataframe(data):
        if "output2" not in data:
            return pd.DataFrame()
        df = pd.DataFrame(data["output2"])
        df = df[["tymd", "xhms", "open", "high", "low", "last", "evol"]]
        df["datetime"] = pd.to_datetime(df["tymd"] + df["xhms"], format="%Y%m%d%H%M%S")
        return df

    exchange_code = "NAS"
    nmin = 1
    max_loops = 3  # 기본 반복 횟수, 필요 시 조절

    all_df = pd.DataFrame()
    first = call_api(exchange_code, stock_code, nmin)
    if not first or "output2" not in first:
        return []

    df = convert_to_dataframe(first)
    all_df = pd.concat([all_df, df], ignore_index=True)
    next_value = first["output1"].get("next", "")
    keyb = get_next_keyb(first["output2"], nmin)

    for _ in range(max_loops - 1):
        next_data = call_api(
            exchange_code, stock_code, nmin, keyb=keyb, next_value=next_value
        )
        if not next_data or "output2" not in next_data:
            break
        df = convert_to_dataframe(next_data)
        all_df = pd.concat([all_df, df], ignore_index=True)
        next_value = next_data["output1"].get("next", "")
        keyb = get_next_keyb(next_data["output2"], nmin)

    all_df.drop_duplicates(inplace=True)
    all_df.sort_values(by="datetime", inplace=True)

    return convert_to_ohlcv_list(all_df)


def compress_to_5min_candles(data):
    df = pd.DataFrame(data)
    df["datetime"] = pd.to_datetime(df["x"], unit="ms")
    df.set_index("datetime", inplace=True)

    df_5min = (
        df.resample("5min")
        .agg({"o": "first", "h": "max", "l": "min", "c": "last", "v": "sum"})
        .dropna()
        .reset_index()
    )

    df_5min["x"] = (df_5min["datetime"].astype(int) / 10**6).astype(int)
    result = df_5min[["x", "o", "h", "l", "c", "v"]].to_dict("records")
    return result


# Helper function to fetch data using yfinance
def get_stock_data_yf(stock_code_yf, period_yf, interval_yf):
    """Fetches stock data using yfinance."""
    try:
        # Ensure stock_code_yf is a string
        if not isinstance(stock_code_yf, str):
            print(f"yfinance Ticker code must be a string. Received: {stock_code_yf}")
            return []

        ticker = yf.Ticker(stock_code_yf)
        hist = ticker.history(period=period_yf, interval=interval_yf)
        if hist.empty:
            print(f"No data from yfinance for {stock_code_yf} with period {period_yf}, interval {interval_yf}")
            return []

        # Convert to required format
        ohlcv_data = []
        for index, row in hist.iterrows():
            # Ensure all expected columns are present and not NaN
            if any(pd.isna(row[col]) for col in ["Open", "High", "Low", "Close", "Volume"]):
                continue # Skip rows with NaN essential values

            ohlcv_data.append({
                "x": int(index.timestamp() * 1000), # Milliseconds timestamp
                "o": float(row["Open"]),
                "h": float(row["High"]),
                "l": float(row["Low"]),
                "c": float(row["Close"]),
                "v": int(row["Volume"]),
            })
        return ohlcv_data
    except Exception as e:
        print(f"Error fetching data from yfinance for {stock_code_yf}: {e}")
        return []


def get_stock_graph(name, period='1d'): # Added period parameter
    jsondata = stock_code_search(name)

    try:
        item = jsondata["result"]["items"][0]
        stock_code = item["code"]
        print(f"[검색된 종목 코드]: {stock_code}")
    except (KeyError, IndexError):
        print("데이터 수신 오류")
        return None

    access_token = load_cached_token() or get_access_token()

    if period == '1m':
        # Determine if it's a domestic Korean stock to append .KS
        # This is a simple heuristic; a more robust way might involve checking market info from stock_code_search
        yf_stock_code = stock_code
        if re.fullmatch(r"\d{6}", stock_code): # Typically 6 digits for KOSPI/KOSDAQ
            # Check if it's likely a KOSPI or KOSDAQ stock from Naver search result if possible
            # For now, assume if numeric it's Korean and needs .KS or .KQ
            # Naver search result might include market name: item.get("marketType") == "KOSPI" or "KOSDAQ"
            market_type = item.get("marketType", "").upper()
            if market_type == "KOSPI":
                 yf_stock_code = f"{stock_code}.KS"
            elif market_type == "KOSDAQ":
                 yf_stock_code = f"{stock_code}.KQ"
            # else, it might be KONEX or other, yfinance might not support it without suffix or at all
            # If no marketType, or it's not KOSPI/KOSDAQ, we might try without suffix or with .KS as a guess
            # For simplicity, if it's all digits and no market type, try .KS
            elif market_type == "": # Fallback for purely numeric codes if marketType is missing
                 yf_stock_code = f"{stock_code}.KS"


        print(f"Fetching 1 month data for {name} (yfinance code: {yf_stock_code})")
        data = get_stock_data_yf(yf_stock_code, period_yf="1mo", interval_yf="1d")
        return data
    elif period == '1y': # Added 1 Year period
        yf_stock_code = stock_code
        if re.fullmatch(r"\d{6}", stock_code):
            market_type = item.get("marketType", "").upper()
            if market_type == "KOSPI":
                 yf_stock_code = f"{stock_code}.KS"
            elif market_type == "KOSDAQ":
                 yf_stock_code = f"{stock_code}.KQ"
            elif market_type == "":
                 yf_stock_code = f"{stock_code}.KS"
        
        print(f"Fetching 1 year data for {name} (yfinance code: {yf_stock_code})")
        data = get_stock_data_yf(yf_stock_code, period_yf="1y", interval_yf="1d") # Fetch daily data for 1 year
        return data
    elif period == '1d': # Default KIS API intraday logic
        if re.fullmatch(r"\d+", stock_code): # Domestic
            data = get_domestic_stock_info(access_token, stock_code)
            return compress_to_5min_candles(data)
        elif re.fullmatch(r"[A-Z.]+", stock_code): # Overseas (currently NAS, uses 1-min data)
            data = get_overseas_stock_info(access_token, stock_code)
            return compress_to_5min_candles(data) # This also compresses to 5min, might need adjustment if original interval is different
        else:
            print("코드 입력 오류 (1d period):", stock_code)
            return None
    else:
        print(f"Unsupported period: {period}")
        return None
