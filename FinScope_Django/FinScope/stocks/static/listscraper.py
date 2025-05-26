"""
⚠️ DEPRECATED FUNCTION WARNING ⚠️

이 함수들은 더 이상 사용되지 않으며, 향후 제거될 예정입니다.
- 현재는 호환성 유지를 위해 남겨져 있습니다.
- 작동을 보장하지 않으며, 유지보수도 제공되지 않습니다.
- 새로운 코드에서는 이 함수들을 사용하지 마세요.

>>> 해당 기능은 향후 코드베이스에서 제거될 수 있습니다.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_hot_stocks():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.get("https://tossinvest.com")
    time.sleep(5)

    stocks = []
    try:
        rows = driver.find_elements(By.CSS_SELECTOR, "#__next tbody tr")

        for row in rows:
            try:
                name = row.find_element(
                    By.CSS_SELECTOR,
                    "td:nth-child(1) > div > div > div:nth-child(3) > span",
                ).text

                price = row.find_element(
                    By.CSS_SELECTOR, "td:nth-child(2) > div > div > span > span"
                ).text

                change = row.find_element(
                    By.CSS_SELECTOR, "td:nth-child(3) > div > div > div > span > span"
                ).text

                stocks.append({"name": name, "price": price, "change": change})
            except Exception as e:
                print("일부 항목 스크래핑 실패:", e)
                continue
    except Exception as e:
        print("접속 실패", e)

    driver.quit()
    return stocks
