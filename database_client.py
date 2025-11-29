# database_client.py
import sqlite3
import json
import os
DB_FILE = os.getenv("DB_FILE", "pizza.db")

def init_db():
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            state TEXT DEFAULT 'WAIT_FOR_PIZZA_NAME',
            order_json TEXT DEFAULT '{}'
        )
    """)
    conn.commit()
    conn.close()

def save_telegram_event(update: dict):
    update_id = update["update_id"]
    raw = json.dumps(update, ensure_ascii=False)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO telegram_events (update_id, raw_update) VALUES (?, ?)",
        (update_id, raw)
    )
    conn.commit()
    conn.close()

def get_user(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT state, order_json FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"state": row[0], "order_json": json.loads(row[1])}
    return None

def create_user(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def update_user(user_id: int, state: str = None, order_json: dict = None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if state is not None and order_json is not None:
        cursor.execute(
            "UPDATE users SET state = ?, order_json = ? WHERE user_id = ?",
            (state, json.dumps(order_json, ensure_ascii=False), user_id)
        )
    elif state is not None:
        cursor.execute("UPDATE users SET state = ? WHERE user_id = ?", (state, user_id))
    elif order_json is not None:
        cursor.execute(
            "UPDATE users SET order_json = ? WHERE user_id = ?",
            (json.dumps(order_json, ensure_ascii=False), user_id)
        )
    conn.commit()
    conn.close()