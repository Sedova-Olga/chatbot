# implementations/postgres_db.py
import os
import json
from contextlib import contextmanager
from interfaces.database import Database
import pg8000


class PostgresDatabase(Database):
    def __init__(self):
        self._host = os.getenv("DB_HOST", "localhost")
        self._port = int(os.getenv("DB_PORT", "5432"))
        self._user = os.getenv("DB_USER", "postgres")
        self._password = os.getenv("DB_PASSWORD", "postgres")
        self._database = os.getenv("DB_NAME", "pizza_bot")
        self._init_tables()

    @contextmanager
    def _get_connection(self):
        conn = pg8000.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database,
        )
        try:
            yield conn
        finally:
            conn.close()

    def _init_tables(self):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id BIGINT PRIMARY KEY,
                        state TEXT,
                        last_message_id INTEGER,
                        order_json TEXT
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS telegram_events (
                        id SERIAL PRIMARY KEY,
                        update_id BIGINT UNIQUE NOT NULL,
                        raw_update TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()

    def get_user(self, user_id):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT state, last_message_id, order_json FROM users WHERE user_id = %s",
                    (user_id,)
                )
                row = cur.fetchone()
                if row:
                    order_json = json.loads(row[2]) if row[2] else {}
                    return {
                        "state": row[0],
                        "last_message_id": row[1],
                        "order_json": order_json
                    }
        return None

    def update_user(self, user_id, **kwargs):
        if not kwargs:
            return
        set_clause = ", ".join(f"{k} = %s" for k in kwargs)
        values = list(kwargs.values()) + [user_id]
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"UPDATE users SET {set_clause} WHERE user_id = %s", values)
                conn.commit()

    def create_user(self, user_id):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING",
                    (user_id,)
                )
                conn.commit()

    def save_telegram_event(self, update: dict):
        update_id = update["update_id"]
        raw = json.dumps(update, ensure_ascii=False)
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO telegram_events (update_id, raw_update) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (update_id, raw)
                )
                conn.commit()