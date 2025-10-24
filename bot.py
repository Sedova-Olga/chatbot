# bot.py
from telegram_api import get_updates, send_message
from database import init_db, save_update

def main():
    print("🚀 Бот запущен. Ожидание сообщений...")
    init_db()
    offset = None

    while True:
        updates = get_updates(offset)
        if not updates or not updates.get("ok"):
            continue

        for update in updates["result"]:
            update_id = update["update_id"]
            offset = update_id + 1

            # Сохраняем ВЕСЬ апдейт
            save_update(update)

            # Эхо-ответ только для текстовых сообщений
            message = update.get("message")
            if message and "text" in message:
                chat_id = message["chat"]["id"]
                text = message["text"]
                send_message(chat_id, text)

if __name__ == "__main__":
    main()