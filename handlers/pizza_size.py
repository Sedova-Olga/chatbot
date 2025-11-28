# handlers/pizza_size.py
from handler import Handler
from telegram_api import answer_callback_query, send_message_with_inline_keyboard
from database_client import get_user, update_user

class PizzaSizeHandler(Handler):
    def check_update(self, update: dict) -> bool:
        return (
            "callback_query" in update
            and update["callback_query"]["data"].startswith("size:")
        )

    def handle_update(self, update: dict):
        cb = update["callback_query"]
        callback_id = cb["id"]
        user_id = cb["from"]["id"]
        chat_id = cb["message"]["chat"]["id"]
        data = cb["data"]

        answer_callback_query(callback_id)

        size_map = {
            "size:S": "S",
            "size:M": "M",
            "size:L": "L"
        }
        size = size_map.get(data, "Неизвестный")

        user_data = get_user(user_id)
        if user_data is None:
            return

        # Сохраняем размер
        user_data["order_json"]["pizza_size"] = size

        # Отправляем кнопки напитков
        send_message_with_inline_keyboard(
            chat_id,
            f"Вы выбрали размер: {size}\n🥤 Выберите напиток:",
            [
                [{"text": "Кола", "callback_data": "drink:cola"}],
                [{"text": "Спрайт", "callback_data": "drink:sprite"}],
                [{"text": "Фанта", "callback_data": "drink:fanta"}],
                [{"text": "Нет", "callback_data": "drink:no"}]
            ]
        )

        update_user(user_id, state="WAIT_FOR_DRINKS", order_json=user_data["order_json"])