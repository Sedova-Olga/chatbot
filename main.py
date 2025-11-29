# main.py
import sqlite3
from dispatcher import Dispatcher
from long_polling import start_long_polling
from database_client import init_db
from handlers.start import StartHandler
from handlers.pizza_name import PizzaNameHandler
from handlers.pizza_size import PizzaSizeHandler
from handlers.drinks import DrinksHandler
from handlers.confirm_order import ConfirmOrderHandler
from handlers.update_database_logger import UpdateDatabaseLogger


def main():
    init_db()
    db = sqlite3.connect("messages.db", check_same_thread=False)
    dp = Dispatcher()
    dp.add_handler(StartHandler(db))
    dp.add_handler(PizzaNameHandler(db))
    dp.add_handler(PizzaSizeHandler(db))
    dp.add_handler(DrinksHandler(db))
    dp.add_handler(ConfirmOrderHandler(db))
    dp.add_handler(UpdateDatabaseLogger("messages.db"))

    start_long_polling(dp)


if __name__ == "__main__":
    main()
