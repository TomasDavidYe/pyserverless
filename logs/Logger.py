from abc import ABC, abstractmethod


class Logger(ABC):
    def __init__(self):
        self.log_file = ''

    def add_to_log_file(self, log_line):
        self.log_file += f'\n{log_line}'

    @abstractmethod
    def info(self, message):
        pass

    @abstractmethod
    def error(self, message):
        pass

    @abstractmethod
    def debug(self, message):
        pass
