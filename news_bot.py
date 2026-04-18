import feedparser
import requests
import os
from groq import Groq

# The secret passwords we saved in GitHub Secrets
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# 1. Get MORE news and MORE details from different sources
links = [
    "http://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.tehrantimes.com/rss"
]

news_text = ""
for link in links:
    feed = feedparser.parse(link)
    # Grab the top 8 articles from each site instead of 3
    for article in feed.entries[:8]: 
        # Check if 'iran' is in the title OR the summary/description
        if "iran" in article.title.lower() or "iran" in article.get('description', '').lower():
            # Send the AI the Title AND the full description for better detail
            news_text += f"Title: {article.title}\nDetails: {article.get('description', '')}\n---\n"

# 2. Ask the AI to write a detailed analysis
client = Groq(api_key=GROQ_API_KEY)

advanced_prompt = f"""
You are an expert geopolitical analyst and an English teacher. 
Read this recent news data about 'Iran':
{news_text}

Write a detailed, comprehensive analysis of the current situation for an intermediate English learner.
Your response MUST include:
1. A deep analysis of the events.
2. Specific names of leaders, organizations, or people mentioned in the news.
3. How different sources are reporting this differently. What are the contrasting viewpoints?
4. Format the text with bold words and bullet points so it is easy to read on a phone.
5. Keep the English at an intermediate level (B1/B2).

At the very end, pick 5 useful English vocabulary words used in your analysis and provide their exact Persian (Farsi) translation.
"""

chat = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": advanced_prompt}]
)
summary = chat.choices[0].message.content

# 3. Send it to your phone!
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
response = requests.post(url, data={"chat_id": CHAT_ID, "text": summary})

# 4. Print the result so we can see if it worked in the GitHub logs
print("Telegram says:", response.text)
