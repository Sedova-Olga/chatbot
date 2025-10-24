# database.py
import sqlite3
import json

DB_NAME = "updates.db"

def init_db():
    """Создаёт таблицу для хранения полных апдейтов."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            update_id INTEGER UNIQUE NOT NULL,
            raw_update TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_update(update: dict):
    """Сохраняет полный JSON-апдейт в базу."""
    update_id = update["update_id"]
    raw = json.dumps(update, ensure_ascii=False)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO updates (update_id, raw_update) VALUES (?, ?)",
        (update_id, raw)
    )
    conn.commit()
    conn.close()