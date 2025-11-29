# handlers/start.py
from handler import Handler
from telegram_api import send_message_with_inline_keyboard, delete_message
from database_client import create_user, get_user, update_user


class StartHandler(Handler):
    def __init__(self, db):
        self.db = db

    def check_update(self, update: dict) -> bool:
        return "message" in update and update["message"].get("text") == "/start"

    def handle_update(self, update: dict):
        user_id = update["message"]["from"]["id"]
        chat_id = update["message"]["chat"]["id"]

        create_user(self.db, user_id)

        user_data = get_user(self.db, user_id)

        last_msg_id = user_data.get("last_message_id")
        if last_msg_id:
            try:
                delete_message(chat_id, last_msg_id)
            except Exception as e:
                print(f"Не удалось удалить сообщение {last_msg_id}: {e}")

        response = send_message_with_inline_keyboard(
            chat_id,
            "🍕 Выберите пиццу:",
            [
                [{"text": "Маргарита", "callback_data": "pizza:margarita"}],
                [{"text": "Пепперони", "callback_data": "pizza:pepperoni"}],
                [{"text": "Гавайская", "callback_data": "pizza:hawaiian"}],
            ],
        )

        new_message_id = None
        if response and response.get("ok"):
            new_message_id = response["result"]["message_id"]

        update_user(
            self.db,
            user_id,
            state="WAIT_FOR_PIZZA_NAME",
            last_message_id=new_message_id,
        )
