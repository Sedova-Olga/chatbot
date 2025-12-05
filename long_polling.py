# long_polling.py
import time
from telegram_api import get_updates
from database_client import save_telegram_event


def start_long_polling(dispatcher):
    offset = None
    print("🍕 Pizza Bot запущен. Ожидание заказов...")
    while True:
        try:
            updates = get_updates(offset)
            for update in updates.get("result", []):
                save_telegram_event(update)
                dispatcher.process_update(update)
                offset = update["update_id"] + 1
        except KeyboardInterrupt:
            print("\n🛑 Бот остановлен.")
            break
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(3)
