# handlers/pizza_size.py
from handler import Handler
from telegram_api import answer_callback_query, send_message_with_inline_keyboard

class PizzaSizeHandler(Handler):
    def check_update(self, update: dict, user_data: dict) -> bool:
        return (
            user_data["state"] == "WAIT_FOR_PIZZA_SIZE"
            and "callback_query" in update
            and update["callback_query"]["data"].startswith("size:")
        )

    def handle_update(self, update: dict, user_data: dict, chat_id: int) -> str | None:
        callback = update["callback_query"]
        callback_id = callback["id"]
        data = callback["data"]
        answer_callback_query(callback_id)

        size_map = {
            "size:S": "S",
            "size:M": "M",
            "size:L": "L"
        }
        pizza_size = size_map.get(data, "S")
        user_data["order_json"]["pizza_size"] = pizza_size

        send_message_with_inline_keyboard(chat_id, "Выберите напиток:", [
            [{"text": "Кола", "callback_data": "drink:cola"}],
            [{"text": "Спрайт", "callback_data": "drink:sprite"}],
            [{"text": "Фанта", "callback_data": "drink:fanta"}],
            [{"text": "Нет", "callback_data": "drink:no"}]
        ])
        return "WAIT_FOR_DRINKS"