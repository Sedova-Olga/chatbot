from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class TelegramClient(ABC):
    @abstractmethod
    def send_message(
        self, chat_id: int, text: str, parse_mode: Optional[str] = None
    ) -> Dict:
        pass

    @abstractmethod
    def send_message_with_inline_keyboard(
        self,
        chat_id: int,
        text: str,
        buttons: List[List[Dict[str, str]]],
        parse_mode: Optional[str] = None,
    ) -> Dict:
        pass

    @abstractmethod
    def delete_message(self, chat_id: int, message_id: int) -> Dict:
        pass

    @abstractmethod
    def answer_callback_query(
        self, callback_id: str, text: Optional[str] = None
    ) -> Dict:
        pass
