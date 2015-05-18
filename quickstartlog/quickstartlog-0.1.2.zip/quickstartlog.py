import os
import sys
import logging
import logging.handlers


if sys.version_info[0] == 3:
    _unicode = str
else:
    _unicode = unicode


__version__ = '0.1.2'


_domain = 'quickstartlog'
_level = logging.INFO
_file_path = os.path.join('var', 'log', 'quickstart.log')
_file_encoding = 'utf8'
_msg_encoding = 'utf8'
_logger = None


def set_domain(domain):
    global _domain
    _domain = domain


def set_level(level):
    global _level
    _level = level


def set_file_path(path):
    global _file_path
    _file_path = path


def set_file_encoding(encoding):
    global _file_encoding
    _file_encoding = encoding


def set_msg_encoding(encoding):
    global _msg_encoding
    _msg_encoding = encoding


def debug(msg, *args, **kwargs):
    _get_logger().debug(_decode(msg), *args, **kwargs)


def info(msg, *args, **kwargs):
    _get_logger().info(_decode(msg), *args, **kwargs)


def warn(msg, *args, **kwargs):
    _get_logger().warn(_decode(msg), *args, **kwargs)


def error(msg, *args, **kwargs):
    _get_logger().error(_decode(msg), *args, **kwargs)


def critical(msg, *args, **kwargs):
    _get_logger().critical(_decode(msg), *args, **kwargs)


def _create_logger():
    logger = logging.getLogger(_domain)
    logger.setLevel(_level)

    formatter = logging.Formatter('[%(asctime)s %(levelname)-5.5s] %(message)s', '%H:%M:%S')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    dir_path = os.path.dirname(_file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    file_handler = logging.handlers.TimedRotatingFileHandler(_file_path, 'D', 1, 30, _file_encoding)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def _get_logger():
    global _logger
    if _logger is None:
        _logger = _create_logger()
    return _logger


def _decode(msg):
    if isinstance(msg, _unicode):
        return msg
    else:
        return msg.decode(_msg_encoding)
