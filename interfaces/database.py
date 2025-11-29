from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Database(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def update_user(self, user_id: int, **kwargs) -> None:
        pass

    @abstractmethod
    def create_user(self, user_id: int) -> None:
        pass
