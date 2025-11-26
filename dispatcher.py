# dispatcher.py
from typing import List
from handler import Handler
from database_client import get_user, create_user, update_user


class Dispatcher:
    def __init__(self):
        self.handlers: List[Handler] = []

    def add_handler(self, handler: Handler):
        self.handlers.append(handler)

    def process_update(self, update: dict):
        message = update.get("message")
        if not message:
            return

        user = message["from"]
        user_id = user["id"]
        chat_id = message["chat"]["id"]

        # Инициализация пользователя в БД, если ещё не существует
        create_user(user_id)
        user_data = get_user(user_id)  # Возвращает dict: {"state": str, "order_json": dict}

        # Поиск и выполнение подходящего хэндлера
        new_state = None
        for handler in self.handlers:
            if handler.check_update(update, user_data):
                new_state = handler.handle_update(update, user_data, chat_id)
                break

        # Сохранение изменений в БД
        if new_state is not None:
            # Состояние изменилось — обновляем и state, и order_json
            update_user(user_id, state=new_state, order_json=user_data["order_json"])
        else:
            # Состояние не изменилось — обновляем только order_json
            update_user(user_id, order_json=user_data["order_json"])