"""이 GEMINI_API_KEY로 실제 사용 가능한 모델 목록을 확인하는 진단용 스크립트."""
import os

from google import genai

api_key = os.environ["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

for model in client.models.list():
    actions = getattr(model, "supported_actions", None) or []
    if "generateContent" in actions:
        print(model.name)
