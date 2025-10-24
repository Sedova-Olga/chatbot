# handlers/database_logger.py
from handler import Handler
from database import save_update

class DatabaseLogger(Handler):
    def check_update(self, update: dict) -> bool:
        return True  # Логируем всё

    def handle_update(self, update: dict) -> bool:
        save_update(update)
        return False  # Продолжить обработку