import logging


class MaxLevel(logging.Filter):
    def __init__(self, max_level):
        self.max_level = max_level if isinstance(max_level, int) else getattr(logging, max_level.upper())
        self.name = 'MaxLevel'
    def filter(self, record):
        return record.levelno <= self.max_level
