"""수집·요약된 기사를 HTML 리포트로 렌더링."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from jinja2 import Environment, FileSystemLoader

from fetch import Article
from sources import TOPICS

KST = ZoneInfo("Asia/Seoul")
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
WORDS_PER_MINUTE = 220  # 한국어 요약 기준 대략치
WEEKDAYS_KO = ["월", "화", "수", "목", "금", "토", "일"]


def render_report(
    articles_by_topic: dict[str, list[Article]],
    summaries_by_topic: dict[str, dict[int, str]],
) -> str:
    now = datetime.now(KST)
    topics_view = []
    total_count = 0
    total_chars = 0

    for topic in TOPICS:
        articles = articles_by_topic.get(topic["id"], [])
        summaries = summaries_by_topic.get(topic["id"], {})
        item_views = []
        for i, article in enumerate(articles):
            summary_ko = summaries.get(i, article.summary[:150])
            item_views.append(
                {
                    "title": article.title,
                    "link": article.link,
                    "source": article.source,
                    "summary_ko": summary_ko,
                }
            )
            total_chars += len(summary_ko) + len(article.title)
        total_count += len(item_views)
        topics_view.append({"id": topic["id"], "title": topic["title"], "articles": item_views})

    read_minutes = max(1, round(total_chars / WORDS_PER_MINUTE))

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.html.j2")
    weekday_ko = WEEKDAYS_KO[now.weekday()]
    return template.render(
        date_str=now.strftime(f"%Y년 %m월 %d일 ({weekday_ko})"),
        generated_at=now.strftime("%Y-%m-%d %H:%M KST"),
        total_count=total_count,
        read_minutes=read_minutes,
        topics=topics_view,
    )
