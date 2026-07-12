"""Daily report 생성 진입점.

docs/index.html (최신본)과 docs/archive/YYYY-MM-DD.html (보관용)을 생성한다.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fetch import fetch_all
from render import render_report
from summarize import summarize_articles

KST = ZoneInfo("Asia/Seoul")
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
ARCHIVE_DIR = DOCS_DIR / "archive"


def build_archive_index() -> None:
    files = sorted(ARCHIVE_DIR.glob("*.html"), reverse=True)
    items = "\n".join(
        f'<li><a href="archive/{f.name}">{f.stem}</a></li>' for f in files
    )
    html = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<title>Daily Report Archive</title></head>
<body>
<h1>지난 리포트</h1>
<p><a href="index.html">최신 리포트로 이동</a></p>
<ul>
{items}
</ul>
</body></html>"""
    (DOCS_DIR / "archive.html").write_text(html, encoding="utf-8")


def main() -> None:
    print("[main] RSS 수집 중...")
    articles_by_topic = fetch_all()
    for topic_id, articles in articles_by_topic.items():
        print(f"  - {topic_id}: {len(articles)}건")

    print("[main] 한국어 요약 생성 중...")
    summaries_by_topic = {
        topic_id: summarize_articles(articles)
        for topic_id, articles in articles_by_topic.items()
    }

    print("[main] HTML 렌더링 중...")
    html = render_report(articles_by_topic, summaries_by_topic)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    (DOCS_DIR / "index.html").write_text(html, encoding="utf-8")

    today = datetime.now(KST).strftime("%Y-%m-%d")
    (ARCHIVE_DIR / f"{today}.html").write_text(html, encoding="utf-8")

    build_archive_index()
    print("[main] 완료: docs/index.html")


if __name__ == "__main__":
    main()
