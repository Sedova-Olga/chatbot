# long_polling.py
from telegram_api import get_updates

def start_long_polling(dispatcher):
    print("🍕 Pizza Bot запущен. Ожидание заказов...")
    offset = None
    while True:
        updates = get_updates(offset)
        if not updates or not updates.get("ok"):
            continue
        for update in updates["result"]:
            offset = update["update_id"] + 1
            dispatcher.process_update(update)