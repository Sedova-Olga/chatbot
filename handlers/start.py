# handlers/start.py
import json
from handler import Handler
from interfaces.telegram import TelegramClient
from interfaces.database import Database

class StartHandler(Handler):
    def __init__(self, telegram: TelegramClient, db: Database):
        self.telegram = telegram
        self.db = db

    def check_update(self, update: dict) -> bool:
        return "message" in update and update["message"].get("text") == "/start"

    def handle_update(self, update: dict):
        user_id = update["message"]["from"]["id"]
        chat_id = update["message"]["chat"]["id"]

        self.db.create_user(user_id)
        user_data = self.db.get_user(user_id)

        last_msg_id = user_data.get("last_message_id") if user_data else None
        if last_msg_id:
            try:
                self.telegram.delete_message(chat_id, last_msg_id)
            except Exception:
                pass

        response = self.telegram.send_message_with_inline_keyboard(
            chat_id,
            "🍕 Выберите пиццу:",
            [
                [{"text": "Маргарита", "callback_data": "pizza:margarita"}],
                [{"text": "Пепперони", "callback_data": "pizza:pepperoni"}],
                [{"text": "Гавайская", "callback_data": "pizza:hawaiian"}]
            ]
        )

        new_msg_id = response["result"]["message_id"] if response.get("ok") else None
        self.db.update_user(
            user_id,
            state="WAIT_FOR_PIZZA_NAME",
            order_json=json.dumps({}),
            last_message_id=new_msg_id
        )