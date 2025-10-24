# handlers/message_text_echo.py
from handler import Handler
from telegram_api import send_message

class MessageTextEcho(Handler):
    def check_update(self, update: dict) -> bool:
        return "message" in update and "text" in update["message"]

    def handle_update(self, update: dict) -> bool:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message["text"]
        send_message(chat_id, text)
        return True  # Обработка завершена