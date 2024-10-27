import logging
from pathlib import Path
from typing import Literal


app_logger = logging.getLogger(name='genai')
app_logger.setLevel(logging.DEBUG)
app_logger.addHandler(logging.NullHandler())


console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(levelname)5s - %(message)s"))

file_handlers = {}

def log_to_console(enable:bool = True):
    global console_handler
    if enable:
        app_logger.addHandler(console_handler)
    else:
        app_logger.removeHandler(console_handler)


def create_file_handler(filename: Path, log_level: Literal[10] = logging.DEBUG):
    handler = logging.FileHandler(filename=filename.as_posix())
    handler.setLevel(log_level)
    handler.setFormatter(
        logging.Formatter('%(asctime)s %(process)5d %(levelname)5s %(message)s [%(filename)s:%(lineno)d]'))
    return handler


def log_to_file(filename: Path, log_level: Literal[10] = logging.DEBUG):
    global file_handlers

    if filename not in file_handlers:
        
        handler = create_file_handler(filename=filename)
        file_handlers[filename] = handler
        app_logger.addHandler(handler)
