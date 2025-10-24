# handlers/message_photo_echo.py
from handler import Handler
from telegram_api import send_photo

class MessagePhotoEcho(Handler):
    def check_update(self, update: dict) -> bool:
        return "message" in update and "photo" in update["message"]

    def handle_update(self, update: dict) -> bool:
        message = update["message"]
        chat_id = message["chat"]["id"]
        # photo — список объектов, самый большой — последний
        photo_list = message["photo"]
        largest_photo = photo_list[-1]  # максимальный по размеру
        file_id = largest_photo["file_id"]
        send_photo(chat_id, file_id)
        return True