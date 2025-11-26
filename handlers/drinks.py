# handlers/drinks.py
from handler import Handler
from telegram_api import send_message

# Допустимые напитки
ALLOWED_DRINKS = {"кола", "спрайт", "фанта", "нет"}

class DrinksHandler(Handler):
    def check_update(self, update: dict, user_data: dict) -> bool:
        return user_data["state"] == "WAIT_FOR_DRINKS"

    def handle_update(self, update: dict, user_data: dict, chat_id: int) -> str | None:
        drink = update.get("message", {}).get("text", "").strip().lower()
        if drink not in ALLOWED_DRINKS:
            send_message(chat_id, f"У нас нет такого напитка.\nДоступные: {', '.join(sorted(ALLOWED_DRINKS))}")
            return None
        user_data["order_json"]["drink"] = drink.capitalize() if drink != "нет" else "—"
        # Показываем заказ
        order = user_data["order_json"]
        text = (
            f"Ваш заказ:\n"
            f"Пицца: {order['pizza_name']}\n"
            f"Размер: {order['pizza_size']}\n"
            f"Напиток: {order['drink']}\n\n"
            f"Подтвердить? Напишите 'Да' или 'Нет'"
        )
        send_message(chat_id, text)
        return "WAIT_FOR_ORDER_APPROVE"