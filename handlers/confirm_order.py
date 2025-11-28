# handlers/confirm_order.py
from handler import Handler
from telegram_api import answer_callback_query, send_message
from database_client import update_user

class ConfirmOrderHandler(Handler):
    def check_update(self, update: dict, user_data: dict) -> bool:
        return (
            user_data["state"] == "WAIT_FOR_ORDER_APPROVE"
            and "callback_query" in update
            and update["callback_query"]["data"] in ("confirm:yes", "confirm:no")
        )

    def handle_update(self, update: dict, user_data: dict, chat_id: int) -> str | None:
        callback = update["callback_query"]
        callback_id = callback["id"]
        data = callback["data"]
        user_id = callback["from"]["id"]
        answer_callback_query(callback_id)

        if data == "confirm:yes":
            send_message(chat_id, "✅ Заказ подтверждён! Приятного аппетита! 🍕🥤\nЧтобы заказать снова — напишите /start")
            return "ORDER_FINISHED"
        elif data == "confirm:no":
            send_message(chat_id, "Заказ отменён!")
            return "ORDER_FINISHED"
        return None