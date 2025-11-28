# dispatcher.py
from typing import List
from handler import Handler
from database_client import get_user, create_user, update_user, save_telegram_event

class Dispatcher:
    def __init__(self):
        self.handlers: List[Handler] = []

    def add_handler(self, handler: Handler):
        self.handlers.append(handler)

    def process_update(self, update: dict):
        save_telegram_event(update)

        if "message" in update:
            msg = update["message"]
            user = msg["from"]
            chat_id = msg["chat"]["id"]
        elif "callback_query" in update:
            cb = update["callback_query"]
            user = cb["from"]
            chat_id = cb["message"]["chat"]["id"]
        else:
            return

        user_id = user["id"]
        create_user(user_id)
        user_data = get_user(user_id)

        new_state = None
        for handler in self.handlers:
            if handler.check_update(update, user_data):
                new_state = handler.handle_update(update, user_data, chat_id)
                break

        if new_state is not None:
            update_user(user_id, state=new_state, order_json=user_data["order_json"])
        else:
            update_user(user_id, order_json=user_data["order_json"])