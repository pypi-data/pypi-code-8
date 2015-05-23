import datetime

__author__ = 'nekmo'

def since(dt):
    return datetime.datetime.now() - dt

def until(dt):
    return dt - datetime.datetime.now()