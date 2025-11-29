 # database_client.py
import sqlite3
import json
import os
DB_FILE = os.getenv("DB_FILE", "messages.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            state TEXT DEFAULT 'WAIT_FOR_PIZZA_NAME',
            order_json TEXT DEFAULT '{}'
        )
    """)
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

def get_user(db, user_id):
    cur = db.execute("SELECT state, last_message_id, order_json FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if row:
        order_json_str = row[2]
        try:
            order_json = json.loads(order_json_str) if order_json_str else {}
        except (TypeError, json.JSONDecodeError):
            order_json = {}
        return {
            "state": row[0],
            "last_message_id": row[1],
            "order_json": order_json
        }
    return None

def create_user(db, user_id):
    db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    db.commit()

def update_user(db, user_id, **kwargs):
    print(f"[DEBUG] Обновление пользователя {user_id}: {kwargs}")
    set_clause = ", ".join([f"{k} = ?" for k in kwargs])
    values = list(kwargs.values()) + [user_id]
    db.execute(f"UPDATE users SET {set_clause} WHERE user_id = ?", values)
    db.commit()

def get_last_message_id(db, user_id):
    cursor = db.execute("SELECT last_message_id FROM user_state WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row and row[0] else None

def save_last_message_id(db, user_id, message_id):
    db.execute("""
        INSERT INTO user_state (user_id, last_message_id)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET last_message_id = ?
    """, (user_id, message_id, message_id))
    db.commit()

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