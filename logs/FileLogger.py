import sys
import os
import logging
from datetime import datetime

from logs.Logger import Logger


class FileLogger(Logger):
    def __init__(self, log_folder, session_name):
        super().__init__()
        self.timeformat = "%Y-%m-%d_%H-%M-%S"
        self.session_name = session_name
        self.log_folder = log_folder
        self.file_name = self.generate_file_name()
        self.logger = self.init_logger()

    def init_logger(self):
        logging.basicConfig(filename=self.file_name,
                            filemode='a',
                            format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt=self.timeformat,
                            level=logging.INFO)

        logger = logging.getLogger(self.session_name)
        logger.addHandler(logging.StreamHandler(sys.stdout))

        return logger


    def info(self, message):
        self.logger.info(message)
        self.add_to_log_file(message)

    def error(self, message):
        self.logger.error(message)
        self.add_to_log_file(message)

    def debug(self, message):
        self.logger.debug(message)
        self.add_to_log_file(message)

    def generate_file_name(self):
        folder_name = f'{self.log_folder}/{self.session_name}'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return f'{folder_name}/{datetime.utcnow().strftime(self.timeformat)}.log'
