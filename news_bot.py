import feedparser, requests, os
from groq import Groq

# The secret passwords we saved earlier
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# 1. Get the news from 3 different places (we can add the other 12 later)
links = [
    "http://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.tehrantimes.com/rss"
]

news_text = ""
for link in links:
    feed = feedparser.parse(link)
    for article in feed.entries[:3]: # grab the top 3 headlines from each
        if "iran" in article.title.lower():
            news_text += article.title + "\n"

# 2. Ask the AI to write a simple summary
client = Groq(api_key=GROQ_API_KEY)
chat = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": f"You are an English teacher. Read these headlines: {news_text}. Write a short summary in simple intermediate English. Then, pick 3 English words you used and translate them to Farsi."}]
)
summary = chat.choices[0].message.content

# 3. Send it to your phone!
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
requests.post(url, data={"chat_id": CHAT_ID, "text": summary})
