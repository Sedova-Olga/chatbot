# database.py
import sqlite3
import json

DB_FILE = "updates.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telegram_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            update_id INTEGER UNIQUE NOT NULL,
            raw_update TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_update(update: dict):
    update_id = update["update_id"]
    raw = json.dumps(update, ensure_ascii=False)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO telegram_updates (update_id, raw_update) VALUES (?, ?)",
        (update_id, raw)
    )
    conn.commit()
    conn.close()