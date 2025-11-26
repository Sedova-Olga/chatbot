# main.py
from dispatcher import Dispatcher
from long_polling import start_long_polling
from database_client import init_db
from handlers.start import StartHandler
from handlers.pizza_name import PizzaNameHandler
from handlers.pizza_size import PizzaSizeHandler
from handlers.drinks import DrinksHandler
from handlers.confirm_order import ConfirmOrderHandler
from handlers.restart import RestartHandler

def main():
    init_db()
    dp = Dispatcher()
    
    # 1. Специальные команды (перезапуск)
    dp.add_handler(RestartHandler())
    
    # 2. Подтверждение заказа (работает в состоянии WAIT_FOR_ORDER_APPROVE)
    dp.add_handler(ConfirmOrderHandler())
    
    # 3. Обычные шаги заказа
    dp.add_handler(StartHandler())
    dp.add_handler(PizzaNameHandler())
    dp.add_handler(PizzaSizeHandler())
    dp.add_handler(DrinksHandler())

    start_long_polling(dp)

if __name__ == "__main__":
    main()