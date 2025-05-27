"""
⚠️ DEPRECATED FUNCTION WARNING ⚠️

이 함수들은 더 이상 사용되지 않으며, 향후 제거될 예정입니다.
- 현재는 호환성 유지를 위해 남겨져 있습니다.
- 작동을 보장하지 않으며, 유지보수도 제공되지 않습니다.
- 새로운 코드에서는 이 함수들을 사용하지 마세요.

>>> 해당 기능은 향후 코드베이스에서 제거될 수 있습니다.
"""

import requests


def get_stock_code(name: str) -> str:
    url = "http://data.krx.co.kr/comm/util/SearchEngine/isuCore.cmd"
    params = {
        "isAutoCom": "true",
        "type": "",
        "solrIsuType": "STK",
        "solrKeyword": name,
        "rows": 20,
        "start": 0,
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "http://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json",
    }

    res = requests.post(url, headers=headers, params=params)
    res.raise_for_status()

    try:
        data = res.json()
        if not data["result"]:
            raise ValueError(f"'{name}'과 관련된 종목을 찾을 수 없습니다.")
        return data["result"][0]["isu_srt_cd"][0]
    except Exception as e:
        print("⚠️ 응답 원본:", res.text[:300])
        raise RuntimeError("종목 코드 추출 실패") from e


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import os
from django.conf import settings


def scroll_page(driver, repeat=5, delay=1.5):
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(repeat):
        body.send_keys(Keys.END)
        time.sleep(delay)


def clean_comments(comments):
    return [c.replace("\n", " ").strip() for c in comments if c.strip()]


def get_stock_detail(name):
    stock_code = get_stock_code(name)
    if not stock_code:
        raise ValueError

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.get("https://tossinvest.com/stocks/A" + stock_code + "/order")
    time.sleep(5)

    try:
        price = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div[1]/main/div/div/div/div[3]/div/div[3]/div[2]/span[1]/span",
        ).text
        change = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div[1]/main/div/div/div/div[3]/div/div[3]/div[2]/span[3]/span",
        ).text
        chart_dir = os.path.join(settings.MEDIA_ROOT, "stocks", "charts")
        os.makedirs(chart_dir, exist_ok=True)
        chart_path = os.path.join(chart_dir, f"{stock_code}.png")
        chart_url = f"/media/stocks/charts/{stock_code}.png"
        chart = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div[1]/main/div/div/div/div[5]/div/div[2]/div/div[2]/div/div[1]/div/div/div",
        )
        chart.screenshot(chart_path)

        return {
            "이름": name,
            "코드": stock_code,
            "가격": price,
            "등락률": change,
            "차트": chart_url,
        }

    finally:
        driver.quit()


def get_stock_comments(name):
    stock_code = get_stock_code(name)

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.get("https://tossinvest.com/stocks/A" + stock_code + "/community")
    time.sleep(3)
    if not stock_code:
        raise ValueError

    scroll_page(driver, repeat=4)  # ← 여기가 핵심!
    time.sleep(1)

    comment_blocks = driver.find_elements(
        By.XPATH,
        "/html/body/div[1]/div[1]/div[1]/main/div/div/div/div[5]/div[1]/div/div/section/section/ul/div/div",
    )

    comments = []
    for block in comment_blocks:
        try:
            text = block.find_element(
                By.XPATH, "./article/div/a/span[2]/span"
            ).text.strip()
            if text:
                comments.append(text)
        except:
            continue

    return clean_comments(comments)
