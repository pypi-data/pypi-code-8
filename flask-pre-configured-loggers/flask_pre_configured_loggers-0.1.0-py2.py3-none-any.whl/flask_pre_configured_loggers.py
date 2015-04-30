__version__ = '0.1.0'


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


def get_mail_handler(app):
    """
    Gets a basic SMTP handler configured for flask logging purposes.
    """

    mail_handler = SMTPHandler((app.config['MAIL_SERVER'],
                                app.config['MAIL_PORT']),
                               app.config['MAIL_DEFAULT_SENDER'],
                               app.config['ADMINS'],
                               '[%s] Error report' %
                                   app.config['SITE_NAME'])
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(
        Formatter(app.config['ERROR_MAIL_FORMAT']))

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

    mail_handler = get_mail_handler(app)
    app.logger.addHandler(mail_handler)


def setup_script_logging(app):
    """Sets up script logging to files / streams."""

    script_log_info_file_handler = RotatingFileHandler(
        path.join(app.config['LOG_FOLDER'], 'script_info.log'),
        maxBytes=100000, backupCount=5)
    script_log_info_file_handler.setLevel(logging.INFO)
    script_log_info_file_handler.setFormatter(Formatter(
        app.config['LOG_FILE_FORMAT'], app.config['LOG_FILE_DATEFMT']))
    script_log_info_file_handler.addFilter(
        LevelSpecificLogFilter(logging.WARNING))

    script_log_error_file_handler = RotatingFileHandler(
        path.join(app.config['LOG_FOLDER'], 'script_error.log'),
        maxBytes=100000, backupCount=5)
    script_log_error_file_handler.setLevel(logging.ERROR)
    script_log_error_file_handler.setFormatter(Formatter(
        app.config['LOG_FILE_FORMAT'], app.config['LOG_FILE_DATEFMT']))

    script_log_info_stream_handler = StreamHandler(
        app.quiet and open(os.devnull, 'a') or sys.stdout)
    script_log_info_stream_handler.setLevel(logging.INFO)
    script_log_info_stream_handler.setFormatter(Formatter(
        app.config['LOG_FILE_FORMAT'], app.config['LOG_FILE_DATEFMT']))
    script_log_info_stream_handler.addFilter(
        LevelSpecificLogFilter(logging.WARNING))

    script_log_error_stream_handler = StreamHandler(
        app.quiet and open(os.devnull, 'a') or sys.stderr)
    script_log_error_stream_handler.setLevel(logging.ERROR)
    script_log_error_stream_handler.setFormatter(Formatter(
        app.config['LOG_FILE_FORMAT'], app.config['LOG_FILE_DATEFMT']))

    script_logger = logging.getLogger('script')
    script_logger.setLevel(logging.INFO)
    script_logger.addHandler(script_log_info_file_handler)
    script_logger.addHandler(script_log_error_file_handler)
    script_logger.addHandler(script_log_info_stream_handler)
    script_logger.addHandler(script_log_error_stream_handler)

    if not app.debug:
        mail_handler = get_mail_handler(app)
        script_logger.addHandler(mail_handler)

    app.script_logger = script_logger

