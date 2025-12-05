# implementations/telegram_api_impl.py
from interfaces.telegram import TelegramClient
from telegram_api import (
    send_message as _send,
    send_message_with_inline_keyboard as _send_inline,
    delete_message as _delete,
    answer_callback_query as _answer,
)


class TelegramApiClient(TelegramClient):
    def send_message(
        self, chat_id: int, text: str, parse_mode: str | None = None
    ) -> dict:
        return _send(chat_id, text, parse_mode=parse_mode)

    def send_message_with_inline_keyboard(
        self, chat_id: int, text: str, buttons: list, parse_mode: str | None = None
    ) -> dict:
        return _send_inline(chat_id, text, buttons)

    def delete_message(self, chat_id: int, message_id: int) -> dict:
        return _delete(chat_id, message_id)

    def answer_callback_query(self, callback_id: str, text: str | None = None) -> dict:
        return _answer(callback_id, text)
