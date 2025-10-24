# handler.py
from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def check_update(self, update: dict) -> bool:
        """Возвращает True, если хэндлер может обработать этот апдейт."""
        pass

    @abstractmethod
    def handle_update(self, update: dict) -> bool:
        """
        Обрабатывает апдейт.
        Возвращает True, если обработка завершена и дальнейшая обработка НЕ нужна.
        Возвращает False, если нужно передать управление следующему хэндлеру.
        """
        pass