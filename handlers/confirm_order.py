# handlers/confirm_order.py
import json
from handler import Handler
from interfaces.telegram import TelegramClient
from interfaces.database import Database


class ConfirmOrderHandler(Handler):
    def __init__(self, telegram: TelegramClient, db: Database):
        self.telegram = telegram
        self.db = db

    def check_update(self, update: dict) -> bool:
        return "callback_query" in update and update["callback_query"][
            "data"
        ].startswith("confirm:")

    def handle_update(self, update: dict):
        cb = update["callback_query"]
        callback_id = cb["id"]
        user_id = cb["from"]["id"]
        chat_id = cb["message"]["chat"]["id"]
        data = cb["data"]

        self.telegram.answer_callback_query(callback_id)

        user_data = self.db.get_user(user_id)
        if not user_data:
            return

        last_msg_id = user_data.get("last_message_id")
        if last_msg_id:
            try:
                self.telegram.delete_message(chat_id, last_msg_id)
            except Exception:
                pass

        order_json = user_data.get("order_json") or {}
        if isinstance(order_json, str):
            order_json = json.loads(order_json)

        pizza_name = order_json.get("pizza_name", "—")
        pizza_size = order_json.get("pizza_size", "—")
        drink = order_json.get("drink", "—")

        if data == "confirm:yes":
            text = (
                "✅ <b>Ваш заказ подтверждён!</b>\n\n"
                "🛒 <b>Состав заказа:</b>\n"
                f"  • 🍕 Пицца: <b>{pizza_name}</b>\n"
                f"  • 📏 Размер: <b>{pizza_size}</b>\n"
                f"  • 🥤 Напиток: <b>{drink}</b>\n\n"
                "Приятного аппетита! 🍕🥤\n"
                "Чтобы заказать снова — напишите <b>/start</b>."
            )
        else:
            text = (
                "❌ <b>Заказ отменён.</b>\n\n"
                "Чтобы заказать снова — напишите <b>/start</b>."
            )

        self.telegram.send_message(chat_id, text, parse_mode="HTML")

        self.db.update_user(
            user_id,
            state="ORDER_FINISHED",
            order_json=json.dumps(order_json, ensure_ascii=False),
            last_message_id=None,
        )
