import logging
import logging.handlers
import os

log_dir = './logs/'


class Logger(logging.Logger):
    def __init__(self, test_name):
        super(Logger, self).__init__(name=test_name, level=logging.DEBUG)

        formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s  %(filename)s:%(lineno)d in %(funcName)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        five_mb = 5000000

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file_handler = logging.handlers.RotatingFileHandler(
            filename=log_dir + test_name + '.log',
            maxBytes=five_mb,
            backupCount=3)

        log_file_handler.setFormatter(formatter)
        super(Logger, self).addHandler(log_file_handler)

