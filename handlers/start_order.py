# handlers/start_order.py
from handler import Handler
from telegram_api import send_message_with_inline_keyboard


class StartOrderHandler(Handler):
    def check_update(self, update: dict, user_data: dict) -> bool:
        # Срабатывает на callback_data = "start_order"
        return (
            "callback_query" in update
            and update["callback_query"]["data"] == "start_order"
        )

    def handle_update(self, update: dict, user_data: dict, chat_id: int) -> str | None:
        # Отправляем выбор пиццы
        send_message_with_inline_keyboard(
            chat_id,
            "Выберите пиццу:",
            [
                [{"text": "Маргарита", "callback_data": "pizza:margarita"}],
                [{"text": "Пепперони", "callback_data": "pizza:pepperoni"}],
                [{"text": "Гавайская", "callback_data": "pizza:hawaiian"}],
            ],
        )
        # Меняем состояние
        return "WAIT_FOR_PIZZA_NAME"
