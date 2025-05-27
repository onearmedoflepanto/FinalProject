import google.generativeai as genai
import json
from decouple import config
import re


def get_recommend(user_info):
    genai.configure(api_key=config("GEMMINI_API_KEY")) # Ensure .env has GEMMINI_API_KEY

    model = genai.GenerativeModel("gemini-1.5-flash-latest") # Changed to a more standard model

    # Construct the absolute path to financial_products.json
    # Assuming this script is in FinScope_Django/stocks/static/
    # and financial_products.json is in FinScope_Django/
    import os
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir = os.path.abspath(os.path.join(current_script_dir, '..', '..')) # FinScope_Django
    json_file_path = os.path.join(project_root_dir, "financial_products.json")

    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            financial_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: financial_products.json not found at {json_file_path}")
        # Return an error structure or raise an exception that the view can catch
        error_response = [{"name": "Financial data not available", "type": "error"}]
        return json.dumps(error_response) # Return as JSON string as the view expects JSON loadable text

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
    try:
        response = model.generate_content(prompt)
        raw_text = response.text
        print("Raw Gemini Response Text:", repr(raw_text))

        # Attempt to extract JSON from the response, as LLMs can sometimes add extra text
        # This regex looks for a string starting with '[' and ending with ']', non-greedily.
        match = re.search(r'\[.*\]', raw_text, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                # Validate if the extracted string is valid JSON
                json.loads(json_str) # This will raise an error if not valid JSON
                return json_str # Return the valid JSON string
            except json.JSONDecodeError as e:
                print(f"Extracted string is not valid JSON: {json_str}. Error: {e}")
                # Fallback or error handling if strict JSON is required by the view
                error_detail = f"AI response format error (extracted part not JSON): {e}"
                return json.dumps([{"name": "AI 추천 형식 오류", "type": "error", "detail": error_detail}])
        else:
            print("No JSON array found in Gemini response.")
            # Fallback or error handling if strict JSON is required
            error_detail = "AI did not return the expected JSON array format."
            return json.dumps([{"name": "AI 추천 형식 오류", "type": "error", "detail": error_detail}])

    except Exception as e:
        print(f"Error during Gemini API call or processing: {e}")
        # Return an error structure that the view can handle
        error_detail = f"Gemini API error: {str(e)}"
        return json.dumps([{"name": "AI 추천 생성 실패", "type": "error", "detail": error_detail}])
