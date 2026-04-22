import requests
from config import TELEGRAM_TOKEN, CHAT_ID

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
MAX_MSG_LEN  = 4096   # Telegram hard limit

def send_message(text: str) -> bool:
    """
    Send text to Telegram. Splits automatically if over 4096 characters.
    Returns True on full success.
    """
    chunks = _split_message(text)
    success = True

    for i, chunk in enumerate(chunks):
        payload = {
            "chat_id":    CHAT_ID,
            "text":       chunk,
            "parse_mode": "HTML",   # supports <b>, <i>, <code>
        }
        resp = requests.post(f"{TELEGRAM_API}/sendMessage", data=payload, timeout=15)

        if resp.status_code != 200:
            print(f"❌ Telegram error on chunk {i+1}: {resp.text}")
            success = False
        else:
            print(f"✅ Chunk {i+1}/{len(chunks)} sent.")

    return success

def _split_message(text: str) -> list[str]:
    """Split long text into Telegram-safe chunks, breaking at newlines."""
    if len(text) <= MAX_MSG_LEN:
        return [text]

    chunks = []
    while text:
        if len(text) <= MAX_MSG_LEN:
            chunks.append(text)
            break
        split_at = text.rfind("\n", 0, MAX_MSG_LEN)
        if split_at == -1:
            split_at = MAX_MSG_LEN
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\n")

    return chunks
