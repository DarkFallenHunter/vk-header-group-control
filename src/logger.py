import logging

from enum import Enum


class LogLevel(Enum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


class Logger:
    def __init__(self, name: str, level: LogLevel, log_format: str, filename: str):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level.value)
        self._level = level

        handler = logging.FileHandler(filename)
        handler.setLevel(level.value)

        formatter = logging.Formatter(log_format, datefmt='%d-%b-%y %H:%M:%S')
        handler.setFormatter(formatter)

        self._logger.addHandler(handler)

    def log(self, message: str):
        self._logger.log(self._level.value, message)
