# handlers/update_database_logger.py
from handler import Handler
from interfaces.database import Database


class UpdateDatabaseLogger(Handler):
    def __init__(self, db: Database):
        self.db: Database = db

    def check_update(self, update: dict) -> bool:
        return True

    def handle_update(self, update: dict) -> None:
        try:
            self.db.save_telegram_event(update)
        except Exception as e:
            print(f"Ошибка при логировании update_id={update.get('update_id')}: {e}")
