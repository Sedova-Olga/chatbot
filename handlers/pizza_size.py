# handlers/pizza_size.py
from handler import Handler
from telegram_api import send_message

class PizzaSizeHandler(Handler):
    def check_update(self, update: dict, user_data: dict) -> bool:
        return user_data["state"] == "WAIT_FOR_PIZZA_SIZE"

    def handle_update(self, update: dict, user_data: dict, chat_id: int) -> str | None:
        text = update.get("message", {}).get("text", "").strip()
        if not text:
            send_message(chat_id, "Пожалуйста, отправьте текстовое сообщение с размером: S, M или L")
            return None
        size = text.upper()
        if size not in {"S", "M", "L"}:
            send_message(chat_id, "Пожалуйста, выберите размер: S, M или L")
            return None
        user_data["order_json"]["pizza_size"] = size
        send_message(chat_id, "Теперь выберите напиток:\nКола, Спрайт, Фанта или Нет")
        return "WAIT_FOR_DRINKS"