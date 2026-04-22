import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID        = os.environ["CHAT_ID"]
GROQ_API_KEY   = os.environ["GROQ_API_KEY"]

MODEL = "llama-3.3-70b-versatile"   # upgraded — much smarter output

# ── RSS Sources ──────────────────────────────────────────────────────────────
# Organised by region so we get genuinely balanced perspectives
RSS_SOURCES = {
    "🇺🇸 US Mainstream": [
        "http://rss.cnn.com/rss/edition_world.rss",
        "https://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml",
        "https://feeds.washingtonpost.com/rss/world",
        "https://feeds.npr.org/1004/rss.xml",
        "https://feeds.a.dj.com/rss/RSSWorldNews.xml",          # Wall Street Journal
        "https://abcnews.go.com/abcnews/internationalheadlines",
        "https://www.cbsnews.com/latest/rss/world",
    ],
    "🇺🇸 US Conservative": [
        "http://feeds.foxnews.com/foxnews/world",
        "https://feeds.feedburner.com/breitbart",
    ],
    "🇬🇧 British / European": [
        "https://www.theguardian.com/world/rss",
        "http://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
        "https://www.france24.com/en/rss",
        "https://rss.dw.com/rdf/rss-en-world",                  # Deutsche Welle
        "https://feeds.reuters.com/reuters/worldNews",
    ],
    "🌍 Middle East / Regional": [
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://english.alarabiya.net/tools/rss",               # Saudi perspective
        "https://www.i24news.com/i24News-English.rss",          # Israeli perspective
    ],
    "🇮🇷 Iranian Media": [
        "https://www.tehrantimes.com/rss",
        "https://en.mehrnews.com/rss",
        "https://ifpnews.com/feed",                              # Iran Front Page
    ],
}

# Keywords to filter relevant articles
KEYWORDS = [
    "iran", "iranian", "tehran", "khamenei", "rouhani", "raisi",
    "irgc", "nuclear", "sanctions", "strait of hormuz", "persian gulf"
]

MAX_ARTICLES_PER_SOURCE = 4   # articles per RSS feed
MAX_TOTAL_ARTICLES      = 40  # hard cap before sending to AI
