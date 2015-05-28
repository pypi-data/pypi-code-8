import os
import sys
import logging
import logging.handlers
import ctypes


__version__ = '0.1.5'


if sys.version_info[0] == 3:
    _unicode = str
else:
    _unicode = unicode


_domain = 'quickstartlog'
_level = logging.INFO
_format = ['[%(asctime)s %(levelname)-5.5s] %(message)s', '%H:%M:%S']
_file_path = os.path.join('var', 'log', 'quickstart.log')
_file_encoding = 'utf8'
_msg_encoding = 'utf8'
_logger = None


class ConsoleColorControl(object):
    def default_color(self):
        pass

    def debug(self):
        self.default_color()

    def info(self):
        self.debug()

    def warn(self):
        self.info()

    def error(self):
        self.debug()

    def critical(self):
        self.error()


class WindowsConsoleColorControl(ConsoleColorControl):
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12

    FOREGROUND_WHITE = 0x0f
    FOREGROUND_RED = 0x0c
    FOREGROUND_GREEN = 0x0a
    FOREGROUND_BLUE = 0x09
    FOREGROUND_YELLOW = 0x0e

    def __init__(self):
        self.handle = ctypes.windll.kernel32.GetStdHandle(self.__class__.STD_ERROR_HANDLE)

    def _set_text_color(self, color):
        ctypes.windll.kernel32.SetConsoleTextAttribute(self.handle, color)

    def default_color(self):
        self._set_text_color(self.__class__.FOREGROUND_WHITE)

    def warn(self):
        self._set_text_color(self.__class__.FOREGROUND_YELLOW)

    def error(self):
        self._set_text_color(self.__class__.FOREGROUND_RED)


_console_color_control = WindowsConsoleColorControl() if os.name == 'nt' else ConsoleColorControl()


def set_domain(domain):
    global _domain
    _domain = domain


def set_level(level):
    global _level
    _level = level


def set_format(fmt=None, datefmt=None):
    global _format
    if fmt is not None:
        _format[0] = fmt
    if datefmt is not None:
        _format[1] = datefmt


def set_file_path(path):
    global _file_path
    _file_path = path


def set_file_encoding(encoding):
    global _file_encoding
    _file_encoding = encoding


def set_msg_encoding(encoding):
    global _msg_encoding
    _msg_encoding = encoding


def set_console_color_control(color_control):
    global _console_color_control
    _console_color_control = color_control


def debug(msg, *args, **kwargs):
    _console_color_control.debug()
    _get_logger().debug(_decode(msg), *args, **kwargs)


def info(msg, *args, **kwargs):
    _console_color_control.info()
    _get_logger().info(_decode(msg), *args, **kwargs)


def warn(msg, *args, **kwargs):
    _console_color_control.warn()
    _get_logger().warn(_decode(msg), *args, **kwargs)


def error(msg, *args, **kwargs):
    _console_color_control.error()
    _get_logger().error(_decode(msg), *args, **kwargs)


def critical(msg, *args, **kwargs):
    _console_color_control.critical()
    _get_logger().critical(_decode(msg), *args, **kwargs)


class ColorStream(object):
    def __init__(self, stream):
        self.used_stream = stream

    def flush(self):
        if self.used_stream and hasattr(self.used_stream, "flush"):
            self.used_stream.flush()

    def write(self, msg):
        self.used_stream.write(msg)


def _create_logger():
    logger = logging.getLogger(_domain)
    logger.setLevel(_level)

    formatter = logging.Formatter(_format[0], _format[1])

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    dir_path = os.path.dirname(_file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    file_handler = logging.handlers.TimedRotatingFileHandler(_file_path, 'D', 1, 30, _file_encoding)
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
