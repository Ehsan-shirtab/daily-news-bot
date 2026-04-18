import feedparser
import requests
import os
from groq import Groq

# The secret passwords we saved in GitHub Secrets
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# 1. 15+ Sources, heavily focused on USA and Western media
links = [
    # USA & Western Media
    "http://rss.cnn.com/rss/edition_world.rss",
    "http://feeds.foxnews.com/foxnews/world",
    "https://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml",
    "https://feeds.washingtonpost.com/rss/world",
    "https://feeds.npr.org/1004/rss.xml",
    "https://www.cbsnews.com/latest/rss/world",
    "https://abcnews.go.com/abcnews/internationalheadlines",
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "https://www.theguardian.com/world/rss",
    "https://www.france24.com/en/rss",
    "https://rss.dw.com/rdf/rss-en-world",
    "http://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
    # Middle Eastern Media
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.tehrantimes.com/rss",
    "https://en.mehrnews.com/rss"
]

news_text = ""
for link in links:
    feed = feedparser.parse(link)
    # Grab the top 5 articles from each to avoid making the text too long for the AI
    for article in feed.entries[:5]: 
        if "iran" in article.title.lower() or "iran" in article.get('description', '').lower():
            news_text += f"Title: {article.title}\nDetails: {article.get('description', '')}\n---\n"

# 2. Ask the AI with the "Goldilocks" Prompt (High Detail, Simple Words)
client = Groq(api_key=GROQ_API_KEY)

goldilocks_prompt = f"""
You are a professional journalist writing for an intermediate English learner (CEFR B1/B2 level).
Read this recent news data about 'Iran':
{news_text}

Write a detailed news report about TODAY'S specific events. 
You MUST follow these strict rules:

1. HIGH DETAIL: Give EXACT details. You must include the specific names of people, exact quotes, numbers, and specific actions happening right now. Do NOT give vague generalities or past history.
2. SIMPLE ENGLISH: Keep the English easy to read. Use short sentences. Do NOT use complex academic or formal words. Use standard, everyday intermediate vocabulary.
3. CONTRAST: Briefly explain how Western news and Middle Eastern news are reporting these exact events differently today.
4. FORMAT: Format the text with clear bold headings and bullet points.

At the very end, pick 5 useful English vocabulary words from your text. Provide their EXACT and NATURAL Persian (Farsi) translation. Use standard Farsi dictionary equivalents, not robotic word-by-word translations.
"""

chat = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": goldilocks_prompt}]
)
summary = chat.choices[0].message.content

# 3. Send it to your phone!
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
response = requests.post(url, data={"chat_id": CHAT_ID, "text": summary})

# 4. Print the result so we can see if it worked in the GitHub logs
print("Telegram says:", response.text)
