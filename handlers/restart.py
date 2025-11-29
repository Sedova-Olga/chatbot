# handlers/restart.py
from handler import Handler
from telegram_api import send_message
from database_client import update_user


class RestartHandler(Handler):
    def check_update(self, update: dict, user_data: dict) -> bool:
        text = update.get("message", {}).get("text", "").lower()
        return "заново" in text or "сначала" in text

    def handle_update(self, update: dict, user_data: dict, chat_id: int) -> str | None:
        user_id = update["message"]["from"]["id"]
        update_user(user_id, state="WAIT_FOR_PIZZA_NAME", order_json={})
        send_message(chat_id, "Начинаем заказ заново! 🍕\nКакую пиццу хотите?")
        return None
