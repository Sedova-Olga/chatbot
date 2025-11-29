# handlers/pizza_name.py
from handler import Handler
from telegram_api import answer_callback_query, send_message_with_inline_keyboard, delete_message
from database_client import get_user, update_user
import json

class PizzaNameHandler(Handler):
    def __init__(self, db):
        self.db = db

    def check_update(self, update: dict) -> bool:
        return (
            "callback_query" in update
            and update["callback_query"]["data"].startswith("pizza:")
        )

    def handle_update(self, update: dict):
        cb = update["callback_query"]
        callback_id = cb["id"]
        user_id = cb["from"]["id"]
        chat_id = cb["message"]["chat"]["id"]
        data = cb["data"]

        answer_callback_query(callback_id)

        pizza_map = {
            "pizza:margarita": "Маргарита",
            "pizza:pepperoni": "Пепперони",
            "pizza:hawaiian": "Гавайская"
        }
        pizza_name = pizza_map.get(data, "Неизвестная")

        user_data = get_user(self.db, user_id)
        if user_data is None:
            return
        
        order_json = user_data.get("order_json") or {}
        order_json["pizza_name"] = pizza_name

        last_msg_id = user_data.get("last_message_id")
        if last_msg_id:
            try:
                delete_message(chat_id, last_msg_id)
            except Exception as e:
                print(f"Не удалось удалить сообщение {last_msg_id}: {e}")

        response = send_message_with_inline_keyboard(
            chat_id,
            f"Вы выбрали: {pizza_name}\n📏 Выберите размер:",
            [
                [{"text": "S", "callback_data": "size:S"}],
                [{"text": "M", "callback_data": "size:M"}],
                [{"text": "L", "callback_data": "size:L"}]
            ]
        )

        new_message_id = response["result"]["message_id"] if response.get("ok") else None

        update_user(
        self.db,
        user_id,
        state="WAIT_FOR_PIZZA_SIZE",
        order_json=json.dumps(order_json, ensure_ascii=False),
        last_message_id=new_message_id
        )