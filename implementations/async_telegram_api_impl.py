# implementations/async_telegram_api_impl.py
import os
import aiohttp
from interfaces.telegram import TelegramClient

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN must be set in environment variables")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


class AsyncTelegramApiClient(TelegramClient):
    def __init__(self):
        self._session = None

    async def _get_session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def send_message(
        self, chat_id: int, text: str, parse_mode: str | None = None
    ) -> dict:
        session = await self._get_session()
        url = f"{BASE_URL}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        if parse_mode:
            payload["parse_mode"] = parse_mode

        from utils import log_execution_time

        @log_execution_time
        async def _inner():
            async with session.post(url, json=payload) as response:
                return await response.json()

        return await _inner()

    async def send_message_with_inline_keyboard(
        self, chat_id: int, text: str, buttons: list
    ) -> dict:
        session = await self._get_session()
        url = f"{BASE_URL}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": {"inline_keyboard": buttons},
        }

        from utils import log_execution_time

        @log_execution_time
        async def _inner():
            async with session.post(url, json=payload) as response:
                return await response.json()

        return await _inner()

    async def delete_message(self, chat_id: int, message_id: int) -> dict:
        session = await self._get_session()
        url = f"{BASE_URL}/deleteMessage"
        payload = {"chat_id": chat_id, "message_id": message_id}

        from utils import log_execution_time

        @log_execution_time
        async def _inner():
            async with session.post(url, json=payload) as response:
                return await response.json()

        return await _inner()

    async def answer_callback_query(
        self, callback_id: str, text: str | None = None
    ) -> dict:
        session = await self._get_session()
        url = f"{BASE_URL}/answerCallbackQuery"
        payload = {"callback_query_id": callback_id}
        if text:
            payload["text"] = text

        from utils import log_execution_time

        @log_execution_time
        async def _inner():
            async with session.post(url, json=payload) as response:
                return await response.json()

        return await _inner()
