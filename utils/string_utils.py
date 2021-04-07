import enum
import json
import string
import random
from datetime import datetime
import time

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def generate_random_string(string_length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def get_sql_list_string_from_python_list(python_list):
    comma_separated = ','.join([f'\'{item}\'' for item in python_list])
    return f"({comma_separated})"


def string_to_date(s: str, time_format=TIME_FORMAT):
    return datetime.strptime(s, time_format)


def date_to_string(d: datetime, time_format=TIME_FORMAT):
    return d.strftime(time_format)


def to_json(s):
    def default_value(o):
        if isinstance(o, enum.Enum):
            return o.value
        else:
            return str(o)

    return json.dumps(s, indent=2, default=default_value)


def to_html(s) -> str:
    return s.replace('\n', '<br>&nbsp;')


def to_html_json(s):
    return to_html(to_json(s))


def time_it(procedure, description, logger):
    procedure_start_time = time.time()
    logger.info('\n')
    logger.info(f'--------------{description} START-----------------------')
    result = procedure()
    logger.info(
        f'--------------{description} END, EXEUCTION_TIME = {time.time() - procedure_start_time}------------------')
    logger.info('\n')
    return result
