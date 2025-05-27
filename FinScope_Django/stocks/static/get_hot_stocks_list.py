import requests
import json
import time
from pathlib import Path
from decouple import config
import json

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


def get_stock_list(market_code="J"):
    access_token = load_cached_token() or get_access_token()

    url = f"{BASE_URL}/uapi/domestic-stock/v1/ranking/fluctuation"
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {access_token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHPST01700000",
        "custtype": "P",
    }
    params = {
        "fid_cond_mrkt_div_code": market_code,
        "fid_input_iscd": "",
    }

    response = requests.get(url, headers=headers, params=params)
    print(response.json())

    if response.status_code == 200:
        data = response.json()
        items = data.get("output", [])[:20]  # 상위 20개 추출
        print(f"{'종목명':<15} {'종목코드':<10} {'현재가':>10} {'등락률(%)':>10}")
        print("-" * 50)
        for item in items:
            name = item.get("hts_kor_isnm", "")
            code = item.get("srtn_cd", "")
            price = item.get("stck_prpr", "")
            rate = item.get("prdy_ctrt", "")
            print(f"{name:<15} {code:<10} {price:>10} {rate:>10}")
    else:
        print(f"요청 실패: {response.status_code} - {response.text}")


get_stock_list()
