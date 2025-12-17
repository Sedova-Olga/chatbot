# main.py
import asyncio
from dotenv import load_dotenv

load_dotenv()

from dispatcher import Dispatcher
from long_polling import start_long_polling

# Асинхронные реализации
from implementations.async_postgres_db import AsyncPostgresDatabase
from implementations.async_telegram_api_impl import AsyncTelegramApiClient

# Обработчики
from handlers.start import StartHandler
from handlers.pizza_name import PizzaNameHandler
from handlers.pizza_size import PizzaSizeHandler
from handlers.drinks import DrinksHandler
from handlers.confirm_order import ConfirmOrderHandler
from handlers.update_database_logger import UpdateDatabaseLogger


async def main():
    # Инициализация зависимостей
    db = AsyncPostgresDatabase()
    telegram = AsyncTelegramApiClient()

    # Настройка диспетчера
    dp = Dispatcher()
    dp.add_handler(UpdateDatabaseLogger(db))        # ← логгер (первым — если Dispatcher останавливается после первого хендлера)
    dp.add_handler(StartHandler(telegram, db))
    dp.add_handler(PizzaNameHandler(telegram, db))
    dp.add_handler(PizzaSizeHandler(telegram, db))
    dp.add_handler(DrinksHandler(telegram, db))
    dp.add_handler(ConfirmOrderHandler(telegram, db))

    # Запуск асинхронного опроса
    await start_long_polling(dp)


if __name__ == "__main__":
    asyncio.run(main())