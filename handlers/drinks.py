# handlers/drinks.py
from handler import Handler
from telegram_api import answer_callback_query, send_message_with_inline_keyboard

class DrinksHandler(Handler):
    def check_update(self, update: dict, user_data: dict) -> bool:
        return (
            user_data["state"] == "WAIT_FOR_DRINKS"
            and "callback_query" in update
            and update["callback_query"]["data"].startswith("drink:")
        )

    def handle_update(self, update: dict, user_data: dict, chat_id: int) -> str | None:
        callback = update["callback_query"]
        callback_id = callback["id"]
        data = callback["data"]
        answer_callback_query(callback_id)

        drink_map = {
            "drink:cola": "Кола",
            "drink:sprite": "Спрайт",
            "drink:fanta": "Фанта",
            "drink:no": "—"
        }
        drink_name = drink_map.get(data, "—")
        user_data["order_json"]["drink"] = drink_name

        order = user_data["order_json"]
        text = (
            f"Ваш заказ:\n"
            f"Пицца: {order['pizza_name']}\n"
            f"Размер: {order['pizza_size']}\n"
            f"Напиток: {order['drink']}"
        )
        send_message_with_inline_keyboard(chat_id, text, [
            [{"text": "✅ Подтвердить", "callback_data": "confirm:yes"}],
            [{"text": "❌ Отменить", "callback_data": "confirm:no"}]
        ])
        return "WAIT_FOR_ORDER_APPROVE"