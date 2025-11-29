# handlers/drinks.py
import json
from handler import Handler
from telegram_api import answer_callback_query, send_message_with_inline_keyboard, delete_message
from database_client import get_user, update_user

class DrinksHandler(Handler):
    def __init__(self, db):
        self.db = db

    def check_update(self, update: dict) -> bool:
        return (
            "callback_query" in update
            and update["callback_query"]["data"].startswith("drink:")
        )

    def handle_update(self, update: dict):
        cb = update["callback_query"]
        callback_id = cb["id"]
        user_id = cb["from"]["id"]
        chat_id = cb["message"]["chat"]["id"]
        data = cb["data"]

        answer_callback_query(callback_id)

        drink_map = {
            "drink:cola": "Кола",
            "drink:sprite": "Спрайт",
            "drink:fanta": "Фанта",
            "drink:no": "—"
        }
        drink = drink_map.get(data, "Неизвестный")

        user_data = get_user(self.db, user_id)
        if user_data is None:
            return

        order_json = user_data.get("order_json") or {}
        if isinstance(order_json, str):
            order_json = json.loads(order_json)

        order_json["drink"] = drink

        last_msg_id = user_data.get("last_message_id")
        if last_msg_id:
            try:
                delete_message(chat_id, last_msg_id)
            except Exception as e:
                print(f"Не удалось удалить сообщение {last_msg_id}: {e}")

        text = (
            f"Ваш заказ:\n"
            f"Пицца: {order_json['pizza_name']}\n"
            f"Размер: {order_json['pizza_size']}\n"
            f"Напиток: {order_json['drink']}\n\n"
            f"Подтвердить?"
        )

        response = send_message_with_inline_keyboard(
            chat_id,
            text,
            [
                [{"text": "✅ Да", "callback_data": "confirm:yes"}],
                [{"text": "❌ Нет", "callback_data": "confirm:no"}]
            ]
        )

        new_message_id = response["result"]["message_id"] if response.get("ok") else None
        update_user(
            self.db,
            user_id,
            state="WAIT_FOR_ORDER_APPROVE",
            order_json=json.dumps(order_json, ensure_ascii=False),
            last_message_id=new_message_id
        )