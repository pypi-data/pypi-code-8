import logging
import os
import sys

logger = logging.getLogger(__name__)

def clear():
    os.system('cls') if os.name == "nt" else sys.stdout.write(os.popen('clear').read())

def log(msg):
    print("%s" % msg)

def info(msg, show_console=False):
    logger.info(msg)
    if show_console:
        print("[info] %s" % msg)

def debug(msg, show_console=False):
    logger.debug(msg)
    if show_console:
        print("[debug] %s" % msg)

def warn(msg, show_console=False):
    logger.warn(msg)
    if show_console:
        print("[warn] %s" % msg)

def error(msg, show_console=False):
    logger.error(msg)
    if show_console:
        print("[error] %s" % msg)
