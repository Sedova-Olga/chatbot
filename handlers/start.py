# handlers/start.py
from handler import Handler
from telegram_api import send_message

class StartHandler(Handler):
    def check_update(self, update: dict, user_dict: dict) -> bool:
        text = update.get("message", {}).get("text", "")
        return text == "/start"

    def handle_update(self, update: dict, user_dict: dict, chat_id: int) -> str:
        send_message(chat_id, "Добро пожаловать в Pizza Shop! 🍕\nКакую пиццу хотите?\nНапример: Маргарита, Пепперони, Гавайская")
        return "WAIT_FOR_PIZZA_NAME"