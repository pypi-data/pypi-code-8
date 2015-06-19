import logging
import logging.config
import logging.handlers
import sys


def get_logger(log_level="DEBUG"):
    logger = logging.getLogger('crowd_pam')
    logger.setLevel(log_level)
    std_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    stdout_hdlr = logging.StreamHandler(sys.stdout)
    stdout_hdlr.setFormatter(std_formatter)
    stdout_hdlr.setLevel(logging.DEBUG)

    platform = sys.platform
    if platform.startswith('darwin'):
        try:
            syslog_hdlr = logging.handlers.SysLogHandler('/var/run/syslog', facility='auth')
            syslog_hdlr.setFormatter(std_formatter)
            logger.addHandler(syslog_hdlr)
        except Exception as e:
            logger.addHandler(stdout_hdlr)
            logger.error("Cannot configure syslog connector")
    elif platform.startswith('linux'):
        try:
            syslog_hdlr = logging.handlers.SysLogHandler('/dev/log', facility='auth')
            syslog_hdlr.setFormatter(std_formatter)
            logger.addHandler(syslog_hdlr)
        except Exception as e:
            logger.addHandler(stdout_hdlr)
            logger.error("Cannot configure syslog connector: {}".format(e))
    else:
        logger.addHandler(stdout_hdlr)
        logger.error("Unsupported platform")
        sys.exit(2)
    return logger
