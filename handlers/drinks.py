# handlers/drinks.py
from handler import Handler
from telegram_api import answer_callback_query, send_message_with_inline_keyboard
from database_client import get_user, update_user

class DrinksHandler(Handler):
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

        user_data = get_user(user_id)
        if user_data is None:
            return

        user_data["order_json"]["drink"] = drink

        # Формируем сообщение с заказом
        order = user_data["order_json"]
        text = (
            f"Ваш заказ:\n"
            f"Пицца: {order['pizza_name']}\n"
            f"Размер: {order['pizza_size']}\n"
            f"Напиток: {order['drink']}\n\n"
            f"Подтвердить?"
        )

        send_message_with_inline_keyboard(
            chat_id,
            text,
            [
                [{"text": "✅ Да", "callback_data": "confirm:yes"}],
                [{"text": "❌ Нет", "callback_data": "confirm:no"}]
            ]
        )

        update_user(user_id, state="WAIT_FOR_ORDER_APPROVE", order_json=user_data["order_json"])