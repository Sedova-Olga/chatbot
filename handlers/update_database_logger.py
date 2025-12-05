# handlers/update_database_logger.py
import json
import sqlite3
from handler import Handler


class UpdateDatabaseLogger(Handler):
    def __init__(self, db_path: str = "messages.db"):
        self.db_path = db_path
        self._init_table()

    def _init_table(self):
        """Создаёт таблицу telegram_events, если её нет."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS telegram_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    update_id INTEGER UNIQUE NOT NULL,
                    raw_update TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.commit()

    def check_update(self, update: dict) -> bool:
        return True

    def handle_update(self, update: dict) -> None:
        update_id = update["update_id"]
        raw = json.dumps(update, ensure_ascii=False, separators=(",", ":"))

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO telegram_events (update_id, raw_update) VALUES (?, ?)",
                    (update_id, raw),
                )
                conn.commit()
        except Exception as e:
            print(f"Ошибка при логировании update_id={update_id}: {e}")
