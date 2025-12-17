# handlers/restart.py
import json
from handler import Handler
from interfaces.telegram import TelegramClient
from interfaces.database import Database


class RestartHandler(Handler):
    def __init__(self, telegram: TelegramClient, db: Database):
        self.telegram = telegram
        self.db = db

    def check_update(self, update: dict) -> bool:
        text = update.get("message", {}).get("text", "").lower()
        return "заново" in text or "сначала" in text

    async def handle_update(self, update: dict) -> None:
        user_id = update["message"]["from"]["id"]
        chat_id = update["message"]["chat"]["id"]

        # Сбрасываем заказ и состояние
        await self.db.update_user(
            user_id,
            state="WAIT_FOR_PIZZA_NAME",
            order_json=json.dumps({}),
            last_message_id=None
        )

        # Отправляем сообщение
        await self.telegram.send_message(
            chat_id,
            "Начинаем заказ заново! 🍕\nКакую пиццу хотите?"
        )