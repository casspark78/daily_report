"""OpenAI API를 이용한 한국어 요약/번역."""
from __future__ import annotations

import json
import os

from fetch import Article

MODEL = os.environ.get("SUMMARY_MODEL", "gpt-4o-mini")

_SYSTEM_PROMPT = (
    "너는 바쁜 직장인을 위한 뉴스 큐레이터다. 주어진 기사 목록 각각을 한국어로 "
    "2문장 이내, 120자 내외로 간결하게 요약하라. 이미 한국어 기사라도 핵심만 "
    "추려 다시 요약한다. 과장 없이 사실 위주로 작성한다. "
    '반드시 JSON 배열로만 답하라. 형식: [{"index": 0, "summary": "..."}, ...]'
)


def _fallback_summary(article: Article) -> str:
    text = article.summary.strip() if article.summary.strip() else f"[원문 제목] {article.title}"
    return text[:150] + ("…" if len(text) > 150 else "")


def summarize_articles(articles: list[Article]) -> dict[int, str]:
    """articles의 인덱스 -> 한국어 요약 딕셔너리를 반환. 실패 시 원문 기반 대체 요약."""
    if not articles:
        return {}

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[summarize] OPENAI_API_KEY가 없어 원문 기반 요약으로 대체합니다.")
        return {i: _fallback_summary(a) for i, a in enumerate(articles)}

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        user_content = json.dumps(
            [
                {"index": i, "title": a.title, "text": a.summary}
                for i, a in enumerate(articles)
            ],
            ensure_ascii=False,
        )
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.3,
        )
        raw = response.choices[0].message.content
        data = json.loads(_extract_json_array(raw))
        return {item["index"]: item["summary"] for item in data}
    except Exception as exc:  # API 오류, 파싱 오류 등은 원문 대체
        print(f"[summarize] 요약 실패, 원문 기반으로 대체합니다: {exc}")
        return {i: _fallback_summary(a) for i, a in enumerate(articles)}


def _extract_json_array(text: str) -> str:
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("응답에서 JSON 배열을 찾지 못했습니다.")
    return text[start : end + 1]
