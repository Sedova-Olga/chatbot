# dispatcher.py
from typing import List
from handler import Handler

class Dispatcher:
    def __init__(self):
        self.handlers: List[Handler] = []

    def add_handler(self, handler: Handler):
        self.handlers.append(handler)

    def process_update(self, update: dict):
        for handler in self.handlers:
            if handler.check_update(update):
                stop = handler.handle_update(update)
                if stop:
                    break