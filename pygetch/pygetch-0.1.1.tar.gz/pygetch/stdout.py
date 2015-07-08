"""
This file contains functions for sensibly printing
text to the console.

The utilities allow you to re-write previously-written
text, all without worrying about newlines, etc.

(c) 2015 Matthew Cotton
"""

import os
import sys

####################################
# META (unix)

def disable_echoing():
    """Disables echoing and the cursor"""
    os.system("stty -echo") # disables echoing
    os.system('tput civis') # disables cursor

def enable_echoing():
    """Enables echoing and the cursor"""
    os.system("stty echo")  # enables echoing
    os.system('tput cnorm') # enables cursor

####################################
# STDOUT

def printsl(string):
    """
    Prints the given string as
    UTF-8-encoded, and flushes STDOUT
    """
    sys.stdout.write(string.encode('utf-8'))
    sys.stdout.flush()

def back(length):
    """
    Returns the command string to move the
    cursor back by <length> places

    IMPLICITY RETURNS TO LEFT BORDER!
    """
    if length == 0:
        return ''
    return '\b'*(length-1) + '\r'

def s_and_back(string):
    """
    Returns the given string followed
    by the correct reset string
    """
    return string + back(len(string))

def clear(length):
    """Returns a screen-wipe for the given length"""
    return s_and_back(' '*length)
