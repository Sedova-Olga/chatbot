# handlers/confirm_order.py
from handler import Handler
from telegram_api import send_message
from database_client import update_user

class ConfirmOrderHandler(Handler):
    def check_update(self, update: dict, user_data: dict) -> bool:
        return user_data["state"] == "WAIT_FOR_ORDER_APPROVE"

    def handle_update(self, update: dict, user_data: dict, chat_id: int) -> str | None:
        text = update.get("message", {}).get("text", "").strip().lower()
        if not text:
            send_message(chat_id, "Пожалуйста, отправьте текстовое сообщение с ответом: 'Да' или 'Нет'")
            return None
        user_id = update["message"]["from"]["id"]
        if "да" in text:
            send_message(chat_id, "✅ Заказ подтверждён! Приятного аппетита! 🍕🥤\nЧтобы заказать снова — напишите /start")
            update_user(user_id, state="ORDER_FINISHED")
            return "ORDER_FINISHED"
        elif "нет" in text:
            send_message(chat_id, "Хорошо! Начнём заново. Какую пиццу хотите?")
            update_user(user_id, state="WAIT_FOR_PIZZA_NAME", order_json={})
            return "WAIT_FOR_PIZZA_NAME"
        else:
            send_message(chat_id, "Пожалуйста, напишите 'Да' или 'Нет'")
            return None