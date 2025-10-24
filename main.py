# main.py
from dispatcher import Dispatcher
from long_polling import start_long_polling
from handlers.database_logger import DatabaseLogger
from handlers.message_text_echo import MessageTextEcho
from handlers.message_photo_echo import MessagePhotoEcho
from database import init_db

def main():
    init_db()
    dp = Dispatcher()
    # Порядок важен: сначала логгер, потом обработчики
    dp.add_handler(DatabaseLogger())
    dp.add_handler(MessageTextEcho())
    dp.add_handler(MessagePhotoEcho())

    start_long_polling(dp)

if __name__ == "__main__":
    main()