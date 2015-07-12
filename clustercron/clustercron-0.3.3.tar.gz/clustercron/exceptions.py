# clustercron/exceptions.py
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# -*- coding: utf-8 -*-

'''
clustercron.exceptions
----------------------
'''


class ClustercronException(Exception):
    '''
    Base exception class. All Clustercron specific expections are subclass by
    this class
    '''


class UnableToGetEC2InstanceIdException(ClustercronException):
    '''
    Raised when instance unable to get ECE instance ID
    '''
