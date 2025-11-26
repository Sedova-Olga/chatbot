# telegram_api.py
import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден в .env")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_updates(offset: int = None) -> dict | None:
    url = f"{BASE_URL}/getUpdates"
    if offset is not None:
        url += f"?offset={offset}"
    try:
        with urllib.request.urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"[API] get_updates error: {e}")
        return None

def send_message(chat_id: int, text: str, reply_markup: dict = None):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    data = urllib.parse.urlencode(payload).encode()
    req = urllib.request.Request(url, data=data)
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"[API] send_message error: {e}")