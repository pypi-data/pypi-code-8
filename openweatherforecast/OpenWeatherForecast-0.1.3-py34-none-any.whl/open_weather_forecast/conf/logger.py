import os
import logging

from epic.sales_epicenter.configuration import get_global_settings
from epic.sales_epicenter.constants import LOGGING_FORMATTER


loggers = {}


def create_logger(target):
    """Creates a new logger"""
    gs = get_global_settings()
    path = gs["logging"]["path"]
    level = gs["logging"]["level"]
    filename = os.path.join(path, "app.log")

    handler = logging.FileHandler(filename=filename)
    handler.setFormatter(logging.Formatter(LOGGING_FORMATTER))
    logger = logging.getLogger(target)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    extra = {"target": target}
    logger = logging.LoggerAdapter(logger, extra)
    return logger


def logger(target='SE'):
    """Returns logger by target
    """
    try:
        return loggers[target]
    except KeyError:
        loggers[target] = create_logger(target)
        return loggers[target]
