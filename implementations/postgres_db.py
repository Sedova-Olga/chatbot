import os
import json
from interfaces.database import Database
import pg8000

class PostgresDatabase(Database):
    def __init__(self):
        self._init_connection()
        self._init_db()

    def _init_connection(self):
        self.conn = pg8000.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            database=os.getenv("DB_NAME", "pizza_bot")
        )

    def _init_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    state TEXT,
                    last_message_id INTEGER,
                    order_json TEXT
                )
            """)
            self.conn.commit()

    def get_user(self, user_id):
        with self.conn.cursor() as cur:
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
        set_clause = ", ".join(f"{k} = %s" for k in kwargs)
        values = list(kwargs.values()) + [user_id]
        with self.conn.cursor() as cur:
            cur.execute(f"UPDATE users SET {set_clause} WHERE user_id = %s", values)
            self.conn.commit()

    def create_user(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (user_id) VALUES (%s) ON CONFLICT DO NOTHING",
                (user_id,)
            )
            self.conn.commit()