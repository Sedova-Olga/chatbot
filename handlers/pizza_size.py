# handlers/pizza_size.py
import json
from handler import Handler
from interfaces.telegram import TelegramClient
from interfaces.database import Database


class PizzaSizeHandler(Handler):
    def __init__(self, telegram: TelegramClient, db: Database):
        self.telegram: TelegramClient = telegram
        self.db: Database = db

    def check_update(self, update: dict) -> bool:
        return (
            "callback_query" in update
            and update["callback_query"]["data"].startswith("size:")
        )

    async def handle_update(self, update: dict):
        cb = update["callback_query"]
        callback_id = cb["id"]
        user_id = cb["from"]["id"]
        chat_id = cb["message"]["chat"]["id"]
        data = cb["data"]

        # Подтверждаем нажатие кнопки
        await self.telegram.answer_callback_query(callback_id)

        size_map = {"size:S": "S", "size:M": "M", "size:L": "L"}
        size = size_map.get(data, "Неизвестный")

        # Получаем данные пользователя
        user_data = await self.db.get_user(user_id)
        if not user_data:
            return

        order_json = user_data.get("order_json") or {}
        order_json["pizza_size"] = size

        # Удаляем предыдущее сообщение (если есть)
        last_msg_id = user_data.get("last_message_id")
        if last_msg_id:
            try:
                await self.telegram.delete_message(chat_id, last_msg_id)
            except Exception:
                pass

        # Отправляем сообщение с выбором напитка
        response = await self.telegram.send_message_with_inline_keyboard(
            chat_id,
            f"Вы выбрали размер: {size}\n🥤 Выберите напиток:",
            [
                [{"text": "Кола", "callback_data": "drink:cola"}],
                [{"text": "Спрайт", "callback_data": "drink:sprite"}],
                [{"text": "Фанта", "callback_data": "drink:fanta"}],
                [{"text": "Нет", "callback_data": "drink:no"}],
            ],
        )

        new_msg_id = response["result"]["message_id"] if response.get("ok") else None

        # Сохраняем состояние
        await self.db.update_user(
            user_id,
            state="WAIT_FOR_DRINKS",
            order_json=json.dumps(order_json, ensure_ascii=False),
            last_message_id=new_msg_id,
        )