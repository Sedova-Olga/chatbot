# dispatcher.py


class Dispatcher:
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    def process_update(self, update):
        for handler in self.handlers:
            if handler.check_update(update):
                handler.handle_update(update)
                break
