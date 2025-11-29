# handlers/update_database_logger.py
import json
import sqlite3
import os
from handler import Handler

DB_FILE = os.getenv("DB_FILE", "pizza.db")


def init_telegram_events_table():
    """Создаёт таблицу telegram_events, если её нет."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telegram_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            update_id INTEGER UNIQUE NOT NULL,
            raw_update TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


class UpdateDatabaseLogger(Handler):
    def __init__(self):
        init_telegram_events_table()

    def check_update(self, update: dict) -> bool:
        # Логируем ВСЕ апдейты
        return True

    def handle_update(self, update: dict) -> None:
        update_id = update["update_id"]
        raw = json.dumps(update, ensure_ascii=False, indent=None)

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO telegram_events (update_id, raw_update) VALUES (?, ?)",
            (update_id, raw)
        )
        conn.commit()
        conn.close()