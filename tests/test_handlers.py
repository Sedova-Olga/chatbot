# tests/test_handlers.py
import json
from unittest.mock import Mock
from handlers.pizza_name import PizzaNameHandler
from handlers.drinks import DrinksHandler
from handlers.start import StartHandler
from implementations.sqlite_db import SqliteDatabase  # ← импортируем реализацию

def test_pizza_name_handler_saves_order():
    telegram = Mock()
    telegram.send_message_with_inline_keyboard.return_value = {"ok": True, "result": {"message_id": 456}}
    telegram.delete_message.return_value = None
    telegram.answer_callback_query.return_value = None

    # Используем РЕАЛИЗАЦИЮ, а не сырое соединение
    db = SqliteDatabase("messages.db")  # ← временная БД в памяти
    db.create_user(123)
    db.update_user(123, state="WAIT_FOR_PIZZA_NAME", order_json="{}", last_message_id=123)

    handler = PizzaNameHandler(telegram, db)

    update = {
        "callback_query": {
            "id": "1",
            "from": {"id": 123},
            "message": {"chat": {"id": 123}},
            "data": "pizza:pepperoni"
        }
    }

    handler.handle_update(update)

    user_data = db.get_user(123)
    order = user_data["order_json"]
    if isinstance(order, str):
        order = json.loads(order)
    assert order["pizza_name"] == "Пепперони"

def test_start_handler_initializes_user_and_sends_pizza_menu():
    import tempfile
    import os
    from unittest.mock import Mock
    from handlers.start import StartHandler
    from implementations.sqlite_db import SqliteDatabase

    telegram = Mock()
    telegram.send_message_with_inline_keyboard.return_value = {"ok": True, "result": {"message_id": 100}}
    telegram.delete_message.return_value = None

    # Создаём временную БД
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        db_path = tmp.name

    try:
        db = SqliteDatabase(db_path)
        handler = StartHandler(telegram, db)

        update = {
            "message": {
                "text": "/start",
                "from": {"id": 555},
                "chat": {"id": 555}
            }
        }

        handler.handle_update(update)

        # Проверяем, что пользователь создан и заказ инициализирован
        user_data = db.get_user(555)
        assert user_data is not None
        assert user_data["state"] == "WAIT_FOR_PIZZA_NAME"
        
        order = user_data["order_json"]
        if isinstance(order, str):
            order = json.loads(order)
        assert order == {}

        # Проверяем, что Telegram вызван с правильными параметрами
        telegram.send_message_with_inline_keyboard.assert_called_once()
        call_args = telegram.send_message_with_inline_keyboard.call_args[0]
        chat_id, text, buttons = call_args

        assert chat_id == 555
        assert "Выберите пиццу" in text
        assert len(buttons) == 3  # Маргарита, Пепперони, Гавайская
        assert buttons[0][0]["callback_data"] == "pizza:margarita"
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)

def test_drinks_handler_saves_drink_and_formats_order():
    import tempfile
    import os
    import json
    from unittest.mock import Mock
    from handlers.drinks import DrinksHandler
    from implementations.sqlite_db import SqliteDatabase

    telegram = Mock()
    telegram.send_message_with_inline_keyboard.return_value = {"ok": True, "result": {"message_id": 999}}
    telegram.delete_message.return_value = None
    telegram.answer_callback_query.return_value = None

    # Создаём временный файл для БД
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        db_path = tmp.name

    try:
        db = SqliteDatabase(db_path)

        # Инициализируем пользователя через методы класса
        db.create_user(789)
        initial_order = {"pizza_name": "Маргарита", "pizza_size": "L"}
        db.update_user(
            789,
            state="WAIT_FOR_DRINKS",
            order_json=json.dumps(initial_order)
        )

        handler = DrinksHandler(telegram, db)
        update = {
            "callback_query": {
                "id": "2",
                "from": {"id": 789},
                "message": {"chat": {"id": 789}},
                "data": "drink:cola"
            }
        }

        handler.handle_update(update)

        # Проверяем результат
        user_data = db.get_user(789)
        order = user_data["order_json"]
        if isinstance(order, str):
            order = json.loads(order)
        assert order["drink"] == "Кола"
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)