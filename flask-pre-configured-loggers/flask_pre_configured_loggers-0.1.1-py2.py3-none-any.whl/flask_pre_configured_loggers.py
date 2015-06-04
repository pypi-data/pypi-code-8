__version__ = '0.1.1'


import sys
from os import path
import logging
from logging import Formatter, StreamHandler
from logging.handlers import SMTPHandler, RotatingFileHandler


class LevelSpecificLogFilter(object):
    """
    Log filter that excludes log messages above a certain level
    (e.g. 'WARNING').
    Copied from:
    http://stackoverflow.com/questions/8162419/
    python-logging-specific-level-only
    """

    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self.__level


def get_mail_handler(config):
    """
    Gets a basic SMTP handler configured for flask logging purposes.
    """

    mail_handler = SMTPHandler((config['MAIL_SERVER'],
                                config['MAIL_PORT']),
                               config['MAIL_DEFAULT_SENDER'],
                               config['ADMINS'],
                               '[%s] Error report' %
                                   config['SITE_NAME'])
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(
        Formatter(config['ERROR_MAIL_FORMAT']))

    return mail_handler


def setup_flask_logging(app):
    """
    Sets up Flask request logging (file-based for all environments,
    and error report emailing for prod environment).
    """

    file_handler = RotatingFileHandler(
        path.join(app.config['LOG_FOLDER'], 'flask_error.log'),
        maxBytes=100000, backupCount=5)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(Formatter(
        app.config['LOG_FILE_FORMAT'], app.config['LOG_FILE_DATEFMT']))
    app.logger.addHandler(file_handler)

    mail_handler = get_mail_handler(app.config)
    app.logger.addHandler(mail_handler)


def get_script_logger(debug=True, quiet=False, config=None):
    """Creates a script logger to log to files / streams."""

    log_file_format = (config
        and config['LOG_FILE_FORMAT']
        or '%(levelname)s %(asctime)s %(message)s')

    log_file_datefmt = (config
        and config['LOG_FILE_DATEFMT']
        or '[%Y-%m-%d %H:%M:%S]')

    script_log_info_file_handler = None

    if config:
        script_log_info_file_handler = RotatingFileHandler(
            path.join(config['LOG_FOLDER'], 'script_info.log'),
            maxBytes=100000, backupCount=5)
        script_log_info_file_handler.setLevel(logging.INFO)
        script_log_info_file_handler.setFormatter(Formatter(
            log_file_format, log_file_datefmt))
        script_log_info_file_handler.addFilter(
            LevelSpecificLogFilter(logging.WARNING))

    script_log_error_file_handler = None

    if config:
        script_log_error_file_handler = RotatingFileHandler(
            path.join(config['LOG_FOLDER'], 'script_error.log'),
            maxBytes=100000, backupCount=5)
        script_log_error_file_handler.setLevel(logging.ERROR)
        script_log_error_file_handler.setFormatter(Formatter(
            log_file_format, log_file_datefmt))

    script_log_info_stream_handler = StreamHandler(
        quiet and open(os.devnull, 'a') or sys.stdout)
    script_log_info_stream_handler.setLevel(logging.INFO)
    script_log_info_stream_handler.setFormatter(Formatter(
        log_file_format, log_file_datefmt))
    script_log_info_stream_handler.addFilter(
        LevelSpecificLogFilter(logging.WARNING))

    script_log_error_stream_handler = StreamHandler(
        quiet and open(os.devnull, 'a') or sys.stderr)
    script_log_error_stream_handler.setLevel(logging.ERROR)
    script_log_error_stream_handler.setFormatter(Formatter(
        log_file_format, log_file_datefmt))

    script_logger = logging.getLogger('script')
    script_logger.setLevel(logging.INFO)

    if config:
        script_logger.addHandler(script_log_info_file_handler)
        script_logger.addHandler(script_log_error_file_handler)

    script_logger.addHandler(script_log_info_stream_handler)
    script_logger.addHandler(script_log_error_stream_handler)

    if (not debug) and config:
        mail_handler = get_mail_handler(config)
        script_logger.addHandler(mail_handler)

    return script_logger


def setup_script_logging(app):
    """Sets up script logging on the app."""

    app.script_logger = get_script_logger(debug=app.debug,
                                          quiet=app.quiet,
                                          config=app.config)
