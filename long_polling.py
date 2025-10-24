# long_polling.py
from telegram_api import get_updates

def start_long_polling(dispatcher):
    print("🚀 Запуск long polling...")
    offset = None
    while True:
        updates = get_updates(offset)
        if not updates or not updates.get("ok"):
            continue

        for update in updates["result"]:
            update_id = update["update_id"]
            offset = update_id + 1
            dispatcher.process_update(update)