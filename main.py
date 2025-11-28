# main.py
from dispatcher import Dispatcher
from long_polling import start_long_polling
from database_client import init_db
from handlers.start import StartHandler
from handlers.pizza_name import PizzaNameHandler
from handlers.pizza_size import PizzaSizeHandler
from handlers.drinks import DrinksHandler
from handlers.confirm_order import ConfirmOrderHandler

def main():
    init_db()
    dp = Dispatcher()
    dp.add_handler(ConfirmOrderHandler())
    dp.add_handler(DrinksHandler())
    dp.add_handler(PizzaSizeHandler())
    dp.add_handler(PizzaNameHandler())
    dp.add_handler(StartHandler())
    start_long_polling(dp)
if __name__ == "__main__":
    main()