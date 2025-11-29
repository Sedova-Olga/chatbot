# implementations/sqlite_db.py
import sqlite3
import json
from interfaces.database import Database


class SqliteDatabase(Database):
    def __init__(self, db_path: str = "messages.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    state TEXT,
                    last_message_id INTEGER,
                    order_json TEXT
                )
            """
            )
            # Также создаём telegram_events, если нужно
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS telegram_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    update_id INTEGER UNIQUE NOT NULL,
                    raw_update TEXT NOT NULL
                )
            """
            )

    def get_user(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT state, last_message_id, order_json FROM users WHERE user_id = ?",
                (user_id,),
            )
            row = cur.fetchone()
            if row:
                order_json = json.loads(row[2]) if row[2] else {}
                return {
                    "state": row[0],
                    "last_message_id": row[1],
                    "order_json": order_json,
                }
        return None

    def update_user(self, user_id, **kwargs):
        set_clause = ", ".join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values()) + [user_id]
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(f"UPDATE users SET {set_clause} WHERE user_id = ?", values)

    def create_user(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
