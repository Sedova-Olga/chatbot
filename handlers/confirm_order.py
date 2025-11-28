# handlers/confirm_order.py
from handler import Handler
from telegram_api import answer_callback_query, send_message
from database_client import get_user, update_user

class ConfirmOrderHandler(Handler):
    def check_update(self, update: dict) -> bool:
        return (
            "callback_query" in update
            and update["callback_query"]["data"].startswith("confirm:")
        )

    def handle_update(self, update: dict):
        cb = update["callback_query"]
        callback_id = cb["id"]
        user_id = cb["from"]["id"]
        chat_id = cb["message"]["chat"]["id"]
        data = cb["data"]

        answer_callback_query(callback_id)

        user_data = get_user(user_id)
        if user_data is None:
            return

        if data == "confirm:yes":
            send_message(chat_id, "✅ Заказ подтверждён! Приятного аппетита! 🍕🥤\nЧтобы заказать снова — напишите /start")
            update_user(user_id, state="ORDER_FINISHED", order_json=user_data["order_json"])
        elif data == "confirm:no":
            send_message(chat_id, "Заказ отменён! \nЧтобы заказать снова — напишите /start")
            update_user(user_id, state="ORDER_FINISHED", order_json=user_data["order_json"])