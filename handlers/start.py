# handlers/start.py
from handler import Handler
from telegram_api import send_message_with_inline_keyboard
from database_client import create_user, update_user

class StartHandler(Handler):
    def check_update(self, update: dict) -> bool:
        return "message" in update and update["message"].get("text") == "/start"

    def handle_update(self, update: dict):
        msg = update["message"]
        user_id = msg["from"]["id"]
        chat_id = msg["chat"]["id"]

        create_user(user_id)
        update_user(user_id, state="WAIT_FOR_PIZZA_NAME")

        send_message_with_inline_keyboard(
            chat_id,
            "🍕 Выберите пиццу:",
            [
                [{"text": "Маргарита", "callback_data": "pizza:margarita"}],
                [{"text": "Пепперони", "callback_data": "pizza:pepperoni"}],
                [{"text": "Гавайская", "callback_data": "pizza:hawaiian"}]
            ]
        )