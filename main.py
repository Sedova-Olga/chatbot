# main.py
from dispatcher import Dispatcher
from long_polling import start_long_polling
from implementations.telegram_api_impl import TelegramApiClient
from handlers.start import StartHandler
from handlers.pizza_name import PizzaNameHandler
from handlers.pizza_size import PizzaSizeHandler
from handlers.drinks import DrinksHandler
from handlers.confirm_order import ConfirmOrderHandler
from handlers.update_database_logger import UpdateDatabaseLogger
from implementations.postgres_db import PostgresDatabase


def main():
    # Инициализация зависимостей
    db = PostgresDatabase()
    telegram = TelegramApiClient()

    # Настройка диспетчера
    dp = Dispatcher()
    dp.add_handler(StartHandler(telegram, db))
    dp.add_handler(PizzaNameHandler(telegram, db))
    dp.add_handler(PizzaSizeHandler(telegram, db))
    dp.add_handler(DrinksHandler(telegram, db))
    dp.add_handler(ConfirmOrderHandler(telegram, db))
    dp.add_handler(UpdateDatabaseLogger("messages.db"))

    # Запуск
    start_long_polling(dp)


if __name__ == "__main__":
    main()
