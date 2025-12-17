# implementations/async_postgres_db.py
import os
import json
import asyncpg
from interfaces.database import Database
from utils import log_execution_time

class AsyncPostgresDatabase(Database):
    def __init__(self):
        self._host = os.getenv("DB_HOST", "localhost")
        self._port = int(os.getenv("DB_PORT", "5432"))
        self._user = os.getenv("DB_USER", "postgres")
        self._password = os.getenv("DB_PASSWORD", "postgres")
        self._database = os.getenv("DB_NAME", "pizza_bot")

    @log_execution_time
    async def _init_db(self):
        conn = await asyncpg.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database
        )
        try:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    state TEXT,
                    last_message_id INTEGER,
                    order_json TEXT
                )
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS telegram_events (
                    id SERIAL PRIMARY KEY,
                    update_id BIGINT UNIQUE NOT NULL,
                    raw_update TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        finally:
            await conn.close()

    @log_execution_time
    async def get_user(self, user_id):
        conn = await asyncpg.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database
        )
        try:
            row = await conn.fetchrow(
                "SELECT state, last_message_id, order_json FROM users WHERE user_id = $1",
                user_id
            )
            if row:
                order_json = json.loads(row[2]) if row[2] else {}
                return {
                    "state": row[0],
                    "last_message_id": row[1],
                    "order_json": order_json
                }
            return None
        finally:
            await conn.close()

    @log_execution_time
    async def update_user(self, user_id, **kwargs):
        if not kwargs:
            return
        set_clause = ", ".join(f"{k} = ${i}" for i, k in enumerate(kwargs.keys(), start=1))
        values = list(kwargs.values()) + [user_id]
        conn = await asyncpg.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database
        )
        try:
            await conn.execute(
                f"UPDATE users SET {set_clause} WHERE user_id = ${len(values)}",
                *values
            )
        finally:
            await conn.close()

    @log_execution_time
    async def create_user(self, user_id):
        conn = await asyncpg.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database
        )
        try:
            await conn.execute(
                "INSERT INTO users (user_id) VALUES ($1) ON CONFLICT (user_id) DO NOTHING",
                user_id
            )
        finally:
            await conn.close()

    @log_execution_time
    async def save_telegram_event(self, update: dict):
        update_id = update["update_id"]
        raw = json.dumps(update, ensure_ascii=False, separators=(",", ":"))
        conn = await asyncpg.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database
        )
        try:
            await conn.execute(
                "INSERT INTO telegram_events (update_id, raw_update) VALUES ($1, $2) ON CONFLICT DO NOTHING",
                update_id, raw
            )
        finally:
            await conn.close()