# handlers/confirm_order.py
from handler import Handler
from telegram_api import answer_callback_query, send_message, delete_message
from database_client import get_user, update_user
import json

class ConfirmOrderHandler(Handler):
    def __init__(self, db):
        self.db = db

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

        user_data = get_user(self.db, user_id)
        if user_data is None:
            return

        last_msg_id = user_data.get("last_message_id")
        if last_msg_id:
            try:
                delete_message(chat_id, last_msg_id)
            except Exception as e:
                print(f"Не удалось удалить сообщение {last_msg_id}: {e}")

        if data == "confirm:yes":
            send_message(chat_id, "✅ Заказ подтверждён! Приятного аппетита! 🍕🥤\nЧтобы заказать снова — напишите /start")
        elif data == "confirm:no":
            send_message(chat_id, "Заказ отменён! \nЧтобы заказать снова — напишите /start")

        update_user(
        self.db,
        user_id,
        state="ORDER_FINISHED",
        order_json=json.dumps(user_data.get("order_json", {}), ensure_ascii=False),
        last_message_id=None
        )