# handlers/start_order.py
import json
from handler import Handler
from interfaces.telegram import TelegramClient
from interfaces.database import Database


class StartOrderHandler(Handler):
    def __init__(self, telegram: TelegramClient, db: Database):
        self.telegram = telegram
        self.db = db

    def check_update(self, update: dict) -> bool:
        return (
            "callback_query" in update
            and update["callback_query"]["data"] == "start_order"
        )

    async def handle_update(self, update: dict) -> None:
        cb = update["callback_query"]
        callback_id = cb["id"]
        user_id = cb["from"]["id"]
        chat_id = cb["message"]["chat"]["id"]

        # Подтверждаем нажатие кнопки
        await self.telegram.answer_callback_query(callback_id)

        # Удаляем предыдущее сообщение (опционально)
        last_msg_id = cb["message"].get("message_id")
        if last_msg_id:
            try:
                await self.telegram.delete_message(chat_id, last_msg_id)
            except Exception:
                pass

        # Отправляем выбор пиццы
        response = await self.telegram.send_message_with_inline_keyboard(
            chat_id,
            "🍕 Выберите пиццу:",
            [
                [{"text": "Маргарита", "callback_data": "pizza:margarita"}],
                [{"text": "Пепперони", "callback_data": "pizza:pepperoni"}],
                [{"text": "Гавайская", "callback_data": "pizza:hawaiian"}],
            ]
        )

        # Сохраняем состояние и сбрасываем заказ
        new_msg_id = response["result"]["message_id"] if response.get("ok") else None
        await self.db.update_user(
            user_id,
            state="WAIT_FOR_PIZZA_NAME",
            order_json=json.dumps({}),
            last_message_at=None,
            last_message_id=new_msg_id
        )