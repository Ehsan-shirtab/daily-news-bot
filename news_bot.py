import feedparser
import requests
import os
from groq import Groq

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

# 2. The NEW Simple English Prompt
client = Groq(api_key=GROQ_API_KEY)

simple_prompt = f"""
You are a friendly English teacher. 
Read this recent news data about 'Iran':
{news_text}

Write a clear and easy-to-understand summary of the current situation. 
Your response MUST follow these strict rules:
1. Use VERY SIMPLE English words (CEFR B1 level). Do not use difficult, formal, or academic words. Keep your sentences short.
2. Tell me the main events in a simple way.
3. Mention the specific names of leaders, organizations, or countries involved.
4. Briefly explain how Western news (like USA) and Middle Eastern news are showing different sides of the story.
5. Format the text with bullet points so it is easy to read.

At the very end, pick 5 useful English words from your text and provide their exact Persian (Farsi) translation.
"""

chat = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": simple_prompt}]
)
summary = chat.choices[0].message.content

# 3. Send to Telegram
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
response = requests.post(url, data={"chat_id": CHAT_ID, "text": summary})
print("Telegram says:", response.text)
