from fetcher    import fetch_news
from summarizer import summarize
from sender     import send_message
from datetime   import datetime

def main():
    print(f"\n{'='*50}")
    print(f"🚀 Iran News Bot starting — {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*50}\n")

    # Step 1 — Fetch
    print("📡 Fetching RSS feeds...")
    news_text, source_map = fetch_news()

    if source_map:
        print("✅ Articles found from:")
        for region, titles in source_map.items():
            print(f"   {region}: {len(titles)} articles")
    else:
        print("⚠️  No relevant articles found.")

    # Step 2 — Summarize
    print("\n🤖 Sending to AI for summarization...")
    summary = summarize(news_text)
    print("✅ Summary generated.")

    # Step 3 — Send
    print("\n📨 Sending to Telegram...")
    ok = send_message(summary)

    if ok:
        print("\n🎉 Done! Message delivered successfully.")
    else:
        print("\n❌ One or more messages failed to send.")

if __name__ == "__main__":
    main()
