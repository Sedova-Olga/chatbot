# handlers/pizza_name.py
from handler import Handler
from telegram_api import answer_callback_query, send_message_with_inline_keyboard
from database_client import get_user, update_user

class PizzaNameHandler(Handler):
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

        # Сохраняем пиццу
        user_data = get_user(user_id)
        if user_data is None:
            return
        user_data["order_json"]["pizza_name"] = pizza_name

        # Отправляем кнопки размера
        send_message_with_inline_keyboard(
            chat_id,
            f"Вы выбрали: {pizza_name}\n📏 Выберите размер:",
            [
                [{"text": "S", "callback_data": "size:S"}],
                [{"text": "M", "callback_data": "size:M"}],
                [{"text": "L", "callback_data": "size:L"}]
            ]
        )
        update_user(user_id, state="WAIT_FOR_PIZZA_SIZE", order_json=user_data["order_json"])