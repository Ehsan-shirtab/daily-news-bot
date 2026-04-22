from groq import Groq
from config import GROQ_API_KEY, MODEL

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are a senior international journalist who writes for a global English-learning audience.
Your reader is a Farsi-speaking adult living in Canada at CEFR B1/B2 English level.

STRICT WRITING RULES:
- Use SHORT sentences (max 20 words each).
- Use SIMPLE vocabulary. No academic or legal jargon.
- Be SPECIFIC: use real names, real numbers, real quotes — never vague phrases like "officials say".
- Be BALANCED and factual. Never take sides.
- Write like a real news article, not a school essay.
"""

def build_prompt(news_text: str) -> str:
    return f"""
Here is today's raw news data about Iran from multiple international sources:

{news_text}

Write a professional news digest with EXACTLY this structure:

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 IRAN NEWS DIGEST
📅 [Today's date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 TOP STORY
[Write 3–4 sentences. Include: WHO did WHAT, WHERE, WHEN, and WHY it matters.
Use exact names, numbers, and quotes if available.]

📰 KEY DEVELOPMENTS TODAY
- [Development 1 — 1–2 sentences, specific facts]
- [Development 2 — 1–2 sentences, specific facts]
- [Development 3 — 1–2 sentences, specific facts]
- [Development 4 — 1–2 sentences, specific facts]

🗣️ HOW THE WORLD IS REPORTING IT

🇺🇸 US / Western View:
[2–3 sentences. What angle are CNN, NYT, Fox, BBC taking?
What words or framing do they use?]

🇮🇷 Iranian / Regional View:
[2–3 sentences. How are Tehran Times, Al Jazeera, or regional
outlets framing the SAME events differently?]

💡 WHY IT MATTERS
[2–3 sentences. Explain the bigger picture in very simple English.
Why should ordinary people care about this today?]

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 ENGLISH VOCABULARY BUILDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pick exactly 5 useful English words or phrases from your text above.
For each one:

🔤 Word: [word]
📖 Meaning: [simple 1-sentence English definition]
✍️ Example: [short natural sentence from today's news context]
🇮🇷 Farsi: [natural Farsi translation — NOT word-by-word, use real dictionary Farsi]

━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPORTANT: If the news data is thin or outdated, say so honestly.
Never invent facts or quotes.
"""

def summarize(news_text: str) -> str:
    if not news_text.strip():
        return (
            "⚠️ No relevant Iran news was found in today's RSS feeds.\n"
            "This can happen if feeds are temporarily unavailable. Try again later."
        )

    prompt = build_prompt(news_text)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt},
            ],
            max_tokens=1800,
            temperature=0.4,    # lower = more factual, less creative
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ AI summarization failed: {e}"
