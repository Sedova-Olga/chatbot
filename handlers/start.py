# handlers/start.py
from handler import Handler
from telegram_api import send_message_with_inline_keyboard

class StartHandler(Handler):
    def check_update(self, update: dict, user_data: dict) -> bool:
        return update.get("message", {}).get("text") == "/start"

    def handle_update(self, update: dict, user_data: dict, chat_id: int) -> str | None:
        send_message_with_inline_keyboard(chat_id, "Выберите пиццу:", [
            [{"text": "Маргарита", "callback_data": "pizza:margarita"}],
            [{"text": "Пепперони", "callback_data": "pizza:pepperoni"}],
            [{"text": "Гавайская", "callback_data": "pizza:hawaiian"}]
        ])
        return "WAIT_FOR_PIZZA_NAME"