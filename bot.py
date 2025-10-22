import os
import json
import sqlite3
import urllib.request
import urllib.parse
import time
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден. Создайте файл .env с токеном.")

DB_FILE = "messages.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            update_id INTEGER UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            username TEXT,
            text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_message(update_id, user_id, username, text):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # INSERT OR IGNORE предотвращает дубли при повторной обработке одного update_id
    cursor.execute(
        "INSERT OR IGNORE INTO messages (update_id, user_id, username, text) VALUES (?, ?, ?, ?)",
        (update_id, user_id, username, text)
    )
    conn.commit()
    conn.close()

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return None

def get_updates(offset=None):
    base_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    url = f"{base_url}?offset={offset}" if offset else base_url
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Ошибка получения обновлений: {e}")
        return {"ok": False}

def main():
    print("✅ Бот запущен. Отправьте сообщение в Telegram.")
    init_db()
    offset = None

    while True:
        updates = get_updates(offset)
        if not updates.get("ok"):
            time.sleep(1)
            continue

        results = updates.get("result", [])
        if not results:
            time.sleep(0.5)
            continue

        max_update_id = 0
        for update in results:
            update_id = update["update_id"]
            if update_id > max_update_id:
                max_update_id = update_id

            message = update.get("message")
            if not message or "text" not in message:
                continue

            user = message["from"]
            user_id = user["id"]
            username = user.get("username", "unknown")
            text = message["text"]
            chat_id = message["chat"]["id"]

            save_message(update_id, user_id, username, text)
            print(f"[{update_id}] [{username}] {text}")
            send_message(chat_id, text)

        offset = max_update_id + 1
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен.")