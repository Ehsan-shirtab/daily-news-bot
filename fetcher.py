import feedparser
import requests
from config import RSS_SOURCES, KEYWORDS, MAX_ARTICLES_PER_SOURCE, MAX_TOTAL_ARTICLES

def _is_relevant(text: str) -> bool:
    """Return True if any keyword appears in the text."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in KEYWORDS)

def fetch_news() -> tuple[str, dict]:
    """
    Fetch RSS feeds, filter for Iran-related articles.

    Returns:
        news_text  – plain-text block ready for the AI prompt
        source_map – { region_label: [article_title, ...] } for the header
    """
    all_articles = []
    source_map   = {}

    for region, feeds in RSS_SOURCES.items():
        region_articles = []

        for url in feeds:
            try:
                feed = feedparser.parse(url)
            except Exception:
                continue

            count = 0
            for entry in feed.entries:
                if count >= MAX_ARTICLES_PER_SOURCE:
                    break

                title       = entry.get("title", "")
                description = entry.get("summary", entry.get("description", ""))
                link        = entry.get("link", "")
                published   = entry.get("published", "")

                if not _is_relevant(title + " " + description):
                    continue

                region_articles.append({
                    "region":      region,
                    "title":       title,
                    "description": description[:500],   # cap length
                    "link":        link,
                    "published":   published,
                })
                count += 1

        if region_articles:
            source_map[region] = [a["title"] for a in region_articles]
            all_articles.extend(region_articles)

        if len(all_articles) >= MAX_TOTAL_ARTICLES:
            break

    # Build the plain-text block for the AI
    news_text = ""
    for a in all_articles[:MAX_TOTAL_ARTICLES]:
        news_text += (
            f"[{a['region']}]\n"
            f"Title: {a['title']}\n"
            f"Published: {a['published']}\n"
            f"Details: {a['description']}\n"
            f"---\n"
        )

    return news_text, source_map
