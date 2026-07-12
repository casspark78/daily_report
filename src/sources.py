"""RSS 소스와 토픽 정의."""

TOPICS = [
    {
        "id": "display",
        "title": "📱 디스플레이·반도체",
        "max_items": 4,
        "feeds": [
            "https://www.oled-info.com/rss.xml",
            "https://rss.etnews.com/Section901.xml",
        ],
        "keywords": [
            "디스플레이", "OLED", "LCD", "마이크로LED", "micro led", "microled",
            "반도체", "파운드리", "패널", "display", "semiconductor", "foundry",
            "삼성디스플레이", "LG디스플레이", "샤프", "BOE", "CSOT",
        ],
    },
    {
        "id": "it",
        "title": "💻 IT·개발·스타트업",
        "max_items": 4,
        "feeds": [
            "https://news.ycombinator.com/rss",
            "https://feeds.feedburner.com/geeknews-feed",
            "https://techcrunch.com/feed/",
        ],
        "keywords": [],
    },
    {
        "id": "ai",
        "title": "🤖 AI·머신러닝",
        "max_items": 4,
        "feeds": [
            "http://export.arxiv.org/rss/cs.AI",
            "https://venturebeat.com/category/ai/feed/",
        ],
        "keywords": [],
    },
    {
        "id": "economy",
        "title": "💰 경제·금융·증시",
        "max_items": 4,
        "feeds": [
            "https://www.yna.co.kr/rss/economy.xml",
            "https://www.mk.co.kr/rss/30000001/",
        ],
        "keywords": [],
    },
    {
        "id": "world",
        "title": "🌍 국내외 시사",
        "max_items": 4,
        "feeds": [
            "https://www.yna.co.kr/rss/international.xml",
            "http://feeds.bbci.co.uk/news/world/rss.xml",
        ],
        "keywords": [],
    },
]

# 토픽당 RSS에서 가져올 최대 원본 기사 수 (필터링 전)
FETCH_PER_FEED = 15
