# handlers/pizza_name.py
from handler import Handler
from telegram_api import answer_callback_query, send_message_with_inline_keyboard

class PizzaNameHandler(Handler):
    def check_update(self, update: dict, user_data: dict) -> bool:
        return (
            user_data["state"] == "WAIT_FOR_PIZZA_NAME"
            and "callback_query" in update
            and update["callback_query"]["data"].startswith("pizza:")
        )

    def handle_update(self, update: dict, user_data: dict, chat_id: int) -> str | None:
        callback = update["callback_query"]
        callback_id = callback["id"]
        data = callback["data"]
        answer_callback_query(callback_id)

        pizza_map = {
            "pizza:margarita": "Маргарита",
            "pizza:pepperoni": "Пепперони",
            "pizza:hawaiian": "Гавайская"
        }
        pizza_name = pizza_map.get(data, "Неизвестная пицца")
        user_data["order_json"]["pizza_name"] = pizza_name

        send_message_with_inline_keyboard(chat_id, "Выберите размер:", [
            [{"text": "S", "callback_data": "size:S"}],
            [{"text": "M", "callback_data": "size:M"}],
            [{"text": "L", "callback_data": "size:L"}]
        ])
        return "WAIT_FOR_PIZZA_SIZE"