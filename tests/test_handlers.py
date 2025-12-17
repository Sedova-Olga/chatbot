# tests/test_handlers.py
import json
import tempfile
import os
import pytest
from unittest.mock import AsyncMock
from handlers.pizza_name import PizzaNameHandler
from handlers.drinks import DrinksHandler
from handlers.start import StartHandler
from implementations.async_postgres_db import AsyncPostgresDatabase


@pytest.mark.asyncio
async def test_pizza_name_handler_saves_order():
    telegram = AsyncMock()
    telegram.send_message_with_inline_keyboard.return_value = {
        "ok": True,
        "result": {"message_id": 456},
    }
    telegram.delete_message.return_value = None
    telegram.answer_callback_query.return_value = None

    # Используем асинхронную БД
    db = AsyncPostgresDatabase()

    # Принудительно создаём таблицы
    await db._init_db()

    await db.create_user(123)
    await db.update_user(
        123, state="WAIT_FOR_PIZZA_NAME", order_json="{}", last_message_id=123
    )

    handler = PizzaNameHandler(telegram, db)

    update = {
        "callback_query": {
            "id": "1",
            "from": {"id": 123},
            "message": {"chat": {"id": 123}},
            "data": "pizza:pepperoni",
        }
    }

    await handler.handle_update(update)

    user_data = await db.get_user(123)
    order = user_data["order_json"]
    if isinstance(order, str):
        order = json.loads(order)
    assert order["pizza_name"] == "Пепперони"


@pytest.mark.asyncio
async def test_start_handler_initializes_user_and_sends_pizza_menu():
    telegram = AsyncMock()
    telegram.send_message_with_inline_keyboard.return_value = {
        "ok": True,
        "result": {"message_id": 100},
    }
    telegram.delete_message.return_value = None

    db = AsyncPostgresDatabase()
    await db._init_db()

    handler = StartHandler(telegram, db)

    update = {
        "message": {"text": "/start", "from": {"id": 555}, "chat": {"id": 555}}
    }

    await handler.handle_update(update)

    user_data = await db.get_user(555)
    assert user_data is not None
    assert user_data["state"] == "WAIT_FOR_PIZZA_NAME"

    order = user_data["order_json"]
    if isinstance(order, str):
        order = json.loads(order)
    assert order == {}

    telegram.send_message_with_inline_keyboard.assert_awaited_once()
    call_args = telegram.send_message_with_inline_keyboard.call_args[0]
    chat_id, text, buttons = call_args

    assert chat_id == 555
    assert "Выберите пиццу" in text
    assert len(buttons) == 3
    assert buttons[0][0]["callback_data"] == "pizza:margarita"


@pytest.mark.asyncio
async def test_drinks_handler_saves_drink_and_formats_order():
    telegram = AsyncMock()
    telegram.send_message_with_inline_keyboard.return_value = {
        "ok": True,
        "result": {"message_id": 999},
    }
    telegram.delete_message.return_value = None
    telegram.answer_callback_query.return_value = None

    db = AsyncPostgresDatabase()
    await db._init_db()

    await db.create_user(789)
    initial_order = {"pizza_name": "Маргарита", "pizza_size": "L"}
    await db.update_user(
        789, state="WAIT_FOR_DRINKS", order_json=json.dumps(initial_order)
    )

    handler = DrinksHandler(telegram, db)
    update = {
        "callback_query": {
            "id": "2",
            "from": {"id": 789},
            "message": {"chat": {"id": 789}},
            "data": "drink:cola",
        }
    }

    await handler.handle_update(update)

    user_data = await db.get_user(789)
    order = user_data["order_json"]
    if isinstance(order, str):
        order = json.loads(order)
    assert order["drink"] == "Кола"