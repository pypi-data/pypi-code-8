# coding=utf-8
from nekbot.core.exceptions import PrintableException
from nekbot.protocols import Message
from nekbot.utils.strings import split_arguments

__author__ = 'nekmo'

import pytest
from nekbot.core.types.argparse import Text


def test_text_all_message():
    """Comprobar si funciona el tipo Text siendo este todo el mensaje
    """
    msg = Message('test', 'spam spam spam', 'test')
    text = Text()
    assert text.parse('spam', ['spam', 'spam'], msg, 1) == 'spam spam spam'


def test_text_second_argument():
    """Probando el tipo text, siendo este el segundo argumento
    """
    msg = Message('test', 'spam spam spam', 'test')
    text = Text()
    assert text.parse('spam', ['spam'], msg, 2) == 'spam spam'


def test_text_min_length():
    """Probando tipo text con mín. de caracteres no satisfecho
    """
    msg = Message('test', 'spam spam spam', 'test')
    text = Text(30)
    with pytest.raises(PrintableException):
        text.parse('spam', ['spam'], msg, 2)


def test_text_max_length():
    """Probar el tipo text con max. de caracteres
    """
    msg = Message('test', 'spam spam spam', 'test')
    text = Text(max_length=6)
    args = ['spam']
    assert text.parse('spam', args, msg, 2) == 'spam s'
    assert args == ['pam']


def test_text_quote():
    """Debería devolverse el texto entero, sin fallar por la comilla
    """
    body = 'nobody\'s specs the spanish inquisition'
    msg = Message('test', body, 'test')
    text = Text()
    args = split_arguments(msg.body)
    assert text.parse(args[0], args[1:], msg, 1) == body


def test_text_no_args():
    """Tras tomarse el texto entero, no deberían quedar argumentos
    """
    body = 'nobody\'s specs the spanish inquisition'
    msg = Message('test', body, 'test')
    text = Text()
    split_args = split_arguments(msg.body)
    args = split_args[1:]
    text.parse(split_args[0], args, msg, 1)
    assert args == []


def test_text_quotes():
    """Debería devolverse la frase original con los quotes
    """
    body = 'spam "spam eggs" spam'
    msg = Message('test', body, 'test')
    text = Text()
    args = split_arguments(msg.body)
    assert text.parse(args[0], args[1:], msg, 1) == body
