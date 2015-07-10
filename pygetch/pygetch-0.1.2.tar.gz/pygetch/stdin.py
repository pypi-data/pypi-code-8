#!/usr/bin/env python
# encoding: utf-8

"""
# TODO: ...
"""

__all__ = ["getch", "getch_timeout", "getch_until_enter", "getpass"]

from .utils       import conversion
from .settings    import settings
from .getch.getch import master_getch

####################################

def getch_ords(timeout=0):
    """Returns the ords of the result of getch"""
    return conversion.ords(master_getch(timeout))

def getch_name(timeout=0):
    """Returns the user-friendly name of the key caught"""
    ords = getch_ords(timeout)
    return settings.KEYS.get(ords, conversion.chars(ords))

####################################
# API functions

def getch_timeout(timeout=0.005):
    """Runs getch with the given timeout"""
    return master_getch(timeout)

def getch():
    """Returns getch with no timeout"""
    return getch_timeout(0) # 0 is infinite

def getch_until_enter(can_delete=False):
    """Runs getch, accumulating chars until an 'enter' key"""
    buff = []

    while True:
        char = getch()
        buff.append(char)

        if char in settings.ENTER_KEYS:
            break
        elif can_delete and char in settings.DELETE_KEYS:
            buff = buff[:-2] # delete the 'DEL' that was added, and the previous
        elif char == settings.CONTROL_C: # arbitrary decision.
            raise KeyboardInterrupt

    return ''.join(buff)

def getpass():
    """Runs getch until a carriage return

    NOTE:  respects the BS/DEL keys"""

    return getch_until_enter(can_delete=True)[:-1] # ignore trailing carriage return
