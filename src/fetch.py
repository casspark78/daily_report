"""RSS 피드 수집 및 토픽별 기사 선별."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone

import feedparser

from sources import FETCH_PER_FEED, TOPICS


@dataclass
class Article:
    topic_id: str
    title: str
    link: str
    summary: str
    source: str
    published: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


def _entry_published(entry) -> datetime:
    for key in ("published_parsed", "updated_parsed"):
        value = getattr(entry, key, None)
        if value:
            return datetime.fromtimestamp(time.mktime(value), tz=timezone.utc)
    return datetime.now(timezone.utc)


def _clean_summary(entry) -> str:
    text = getattr(entry, "summary", "") or getattr(entry, "description", "")
    # 아주 단순한 태그 제거 (본격적인 HTML 파싱은 불필요)
    import re

    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    # Hacker News 등 일부 피드는 본문 없이 "Comments" 링크 텍스트만 제공한다.
    if len(text) < 15 or text.lower() in {"comments", "discuss"}:
        return ""
    return text[:600]


def _matches_keywords(article: Article, keywords: list[str]) -> bool:
    if not keywords:
        return True
    haystack = f"{article.title} {article.summary}".lower()
    return any(kw.lower() in haystack for kw in keywords)


def fetch_topic_articles(topic: dict) -> list[Article]:
    candidates: list[Article] = []
    for feed_url in topic["feeds"]:
        try:
            parsed = feedparser.parse(feed_url)
        except Exception as exc:  # 네트워크/파싱 오류는 건너뜀
            print(f"[fetch] {feed_url} 실패: {exc}")
            continue

        source_name = parsed.feed.get("title", feed_url) if parsed.feed else feed_url
        for entry in parsed.entries[:FETCH_PER_FEED]:
            article = Article(
                topic_id=topic["id"],
                title=getattr(entry, "title", "(제목 없음)").strip(),
                link=getattr(entry, "link", ""),
                summary=_clean_summary(entry),
                source=source_name,
                published=_entry_published(entry),
            )
            candidates.append(article)

    filtered = [a for a in candidates if _matches_keywords(a, topic["keywords"])]
    filtered.sort(key=lambda a: a.published, reverse=True)
    return filtered[: topic["max_items"]]


def fetch_all() -> dict[str, list[Article]]:
    result: dict[str, list[Article]] = {}
    for topic in TOPICS:
        result[topic["id"]] = fetch_topic_articles(topic)
    return result
