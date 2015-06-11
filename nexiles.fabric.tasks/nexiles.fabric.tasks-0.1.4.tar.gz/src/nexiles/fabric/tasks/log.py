import logging

from fabric.colors import red, green, yellow, blue

logger = logging.getLogger("nexiles.fabric.tasks")

__all__ = ["setup_logging"]


def setup_logging(logfile="build.log", level=logging.ERROR):
    if logfile is None:
        logging.basicConfig(level=level, format="%(asctime)s [%(levelname)-7s] [line %(lineno)d] %(name)s: %(message)s")
    else:
        logging.basicConfig(filename=logfile, level=level, format="%(asctime)s [%(levelname)-7s] [line %(lineno)d] %(name)s: %(message)s")


def error(message):
    logger.error(message)
    print red(message)


def warning(message):
    logger.warn(message)
    print yellow(message)


def info(message):
    logger.info(message)
    print green(message)


def trace(message):
    logger.debug(message)
    print blue(message)

# EOF
