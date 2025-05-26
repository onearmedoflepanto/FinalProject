from openai import OpenAI
from decouple import config
import json


client = OpenAI(api_key=config("OPENAI_API_KEY"))


def analyze_stock_comments(comments: list[str]) -> dict:
    joined_comments = "\n".join(comments)
    prompt = f"""
다음은 주식 관련 커뮤니티에서 모은 댓글들이야:

{joined_comments}

이 댓글들의 전반적인 분위기를 150자 이내로 요약하고, 마지막에는 긍정/부정/중립 중 1가지 평가를 덧붙여줘.
투자 분위기를 반영한 주식 온도를 0부터 100 사이 정수로 표현해줘.
답변은 반드시 아래 JSON 형식으로 해줘. 그러지 않을 경우 오류가 발생할 수 있어.:

{{
  "summary": "...",
  "temperature": 정수
}}
    """

    response = client.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}], temperature=0.5
    )

    try:
        content = response.choices[0].message.content
        return json.loads(content)
    except:
        return {"summary": "내용 없음", "temperature": 0}
