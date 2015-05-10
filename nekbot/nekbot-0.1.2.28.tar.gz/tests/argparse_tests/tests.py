# coding=utf-8
from nekbot.core.exceptions import PrintableException
from nekbot.core.types.argparse import Text
from nekbot.protocols import Message

__author__ = 'nekmo'

import pytest
from nekbot.core.commands import argparse

def test_without_args():
    """Sin dar argumentos, no debe devolver, ni debe pedir.
    """
    def myfunction(msg):
        pass
    parser = argparse.ArgParse()
    parser.set_from_function(myfunction)
    assert parser.parse([]) == []


def test_arg():
    """Debe devolver el argumento entregado.
    """
    def myfunction(msg, word):
        pass
    parser = argparse.ArgParse()
    parser.set_from_function(myfunction)
    assert parser.parse(['word']) == ['word']


def test_int_arg():
    """Debe devolver el argumento como un int.
    """
    def myfunction(msg, number):
        pass
    parser = argparse.ArgParse()
    parser.set_arg_types([int])
    parser.set_from_function(myfunction)
    assert parser.parse(['1']) == [1]


def test_not_enought_arguments():
    """Si no hay suficientes argumentos, debe fallar.
    """
    def myfunction(msg, word1, word2):
        pass
    parser = argparse.ArgParse()
    parser.set_arg_types([int])
    parser.set_from_function(myfunction)
    with pytest.raises(PrintableException):
        parser.parse(['arg'])


def test_multiple_args():
    """Debe ser capaz de capturar todos los argumentos con *args
    """
    def myfunction(*args):
        pass
    parser = argparse.ArgParse()
    parser.set_from_function(myfunction)
    parser.parse(['spam', 'eggs', 'spam']) == ['spam', 'eggs', 'spam']


def test_detect_kwarg_type():
    """Debe transformar el kwarg opcional en un número
    """
    def myfunction(number=5):
        pass
    parser = argparse.ArgParse()
    parser.set_from_function(myfunction)
    parser.parse(['6']) == [6]


def test_not_require_kwargs():
    """Los kwargs no son obligatorios
    """
    def myfunction(number=5):
        pass
    parser = argparse.ArgParse()
    parser.set_from_function(myfunction)
    parser.parse([]) == []


def test_text_argument():
    """Debería devolverse un único argumento con todo el texto
    """
    def myfunction(text):
        pass
    text = 'nobody\'s specs the spanish inquisition'
    msg = Message('test', text, 'test')
    parser = argparse.ArgParse()
    parser.set_arg_types([Text()])
    parser.set_from_function(myfunction)
    assert parser.parse(text.split(' '), msg) == [text]
