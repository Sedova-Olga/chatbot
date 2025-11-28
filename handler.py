# handler.py
from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def check_update(self, update: dict, user_data: dict) -> bool:
        pass

    @abstractmethod
    def handle_update(self, update: dict, user_data: dict, chat_id: int) -> str | None:
        pass