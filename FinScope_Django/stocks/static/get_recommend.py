import google.generativeai as genai
import json
from decouple import config
import re


def get_recommend(user_info):
    genai.configure(api_key=config("GEMMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

    with open("financial_products.json", "r", encoding="utf-8") as file:
        financial_data = json.load(file)

    financial_data_str = json.dumps(financial_data, ensure_ascii=False, indent=2)

    prompt = (
        json.dumps(user_info, ensure_ascii=False, indent=2)
        + f"""
이것들은 사용자의 투자 성향이야.
그리고 이 목록들은 예/적금과 상위 주식들의 목록이야:
{financial_data_str}

이 중에서 10개 종목을 선정해서 포트폴리오를 구성해 줘.
예/적금의 비율은 최소 3개를 넘어야 해.
정확히 아래 형식의 JSON 배열로만 답해줘. 예시는 다음과 같아:

[
{{"name": "삼성전자", "type": "stock"}},
{{"name": "Sh적금", "type": "deposit"}}
]

이외의 텍스트는 절대 포함하지 마. 오직 위 구조의 JSON 배열만 응답해줘.
    """
    )
    response = model.generate_content(prompt)
    print(response.text)

    return response.text
