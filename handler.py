# handler.py
from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def check_update(self, update: dict, user_dict: dict) -> bool:
        """Проверяет, может ли хэндлер обработать этот апдейт."""
        pass

    @abstractmethod
    def handle_update(self, update: dict, user_dict: dict, chat_id: int) -> str | None:
        """
        Обрабатывает апдейт.
        Возвращает новое состояние (str), если нужно его изменить.
        Возвращает None, если состояние не меняется.
        """
        pass