# handlers/pizza_name.py
from handler import Handler
from telegram_api import send_message

# Допустимые названия пицц
ALLOWED_PIZZAS = {"маргарита", "пепперони", "гавайская"}

class PizzaNameHandler(Handler):
    def check_update(self, update: dict, user_data: dict) -> bool:
        return user_data["state"] == "WAIT_FOR_PIZZA_NAME"

    def handle_update(self, update: dict, user_data: dict, chat_id: int) -> str | None:
        pizza = update.get("message", {}).get("text", "").strip().lower()
        if pizza not in ALLOWED_PIZZAS:
            send_message(chat_id, f"Извините, у нас нет такой пиццы.\nДоступные варианты:\n{', '.join(sorted(ALLOWED_PIZZAS))}")
            return None  # не меняем состояние
        user_data["order_json"]["pizza_name"] = pizza.capitalize()
        send_message(chat_id, f"Отлично! Вы выбрали: {pizza.capitalize()}\nТеперь укажите размер: S, M, L")
        return "WAIT_FOR_PIZZA_SIZE"