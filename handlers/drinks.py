# handlers/drinks.py
import json
from handler import Handler
from interfaces.telegram import TelegramClient
from interfaces.database import Database


class DrinksHandler(Handler):
    def __init__(self, telegram: TelegramClient, db: Database):
        self.telegram = telegram
        self.db = db

    def check_update(self, update: dict) -> bool:
        return "callback_query" in update and update["callback_query"][
            "data"
        ].startswith("drink:")

    def handle_update(self, update: dict):
        cb = update["callback_query"]
        callback_id = cb["id"]
        user_id = cb["from"]["id"]
        chat_id = cb["message"]["chat"]["id"]
        data = cb["data"]

        self.telegram.answer_callback_query(callback_id)

        drink_map = {
            "drink:cola": "Кола",
            "drink:sprite": "Спрайт",
            "drink:fanta": "Фанта",
            "drink:no": "—",
        }
        drink = drink_map.get(data, "—")

        user_data = self.db.get_user(user_id)
        if not user_data:
            return

        order_json = user_data.get("order_json") or {}
        order_json["drink"] = drink

        last_msg_id = user_data.get("last_message_id")
        if last_msg_id:
            try:
                self.telegram.delete_message(chat_id, last_msg_id)
            except Exception:
                pass

        text = (
            f"Ваш заказ:\n\n"
            f"• Пицца: {order_json.get('pizza_name', '—')}\n"
            f"• Размер: {order_json.get('pizza_size', '—')}\n"
            f"• Напиток: {drink}\n\n"
            "Подтвердить заказ?"
        )

        buttons = [
            [{"text": "✅ Да", "callback_data": "confirm:yes"}],
            [{"text": "❌ Нет", "callback_data": "confirm:no"}],
        ]

        response = self.telegram.send_message_with_inline_keyboard(
            chat_id, text, buttons
        )

        new_msg_id = response["result"]["message_id"] if response.get("ok") else None

        self.db.update_user(
            user_id,
            state="WAIT_FOR_ORDER_APPROVE",
            order_json=json.dumps(order_json, ensure_ascii=False),
            last_message_id=new_msg_id,
        )
