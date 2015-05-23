# coding=utf-8
import copy
from random import choice, randint
import re
import requests
from nekbot.core.commands import command
from nekbot.core.exceptions import InvalidArgument

__author__ = 'nekmo'

ERRORS = [
    'Error. Cerebro del usuario < 0.',
    'lim x -> 0; f(x) = 1 / x',
    '0.00000000000000000000000001',
]


def isnumber(val):
    return bool(re.match('^\-?\d+$', val))


@command
def random(msg, *args):
    if not args:
        args = [1, 6]  # Mostraremos un número del 1 al 6
    elif len(args) <= 1 and not args[0].isdigit():
        raise InvalidArgument('Para usar este comando con palabras, debe añadir al menos 2, '
                              'y para números entre 2 rangos, los valores deben ser de tipo '
                              'numérico.', args[0])
    elif len(args) <= 1:
        args = (1, args[0])
    elif not isnumber(args[0]) or not isnumber(args[1]):
        return choice(args)
    min, max = map(int, args)
    if min > max:
        raise InvalidArgument('Excepción: %s' % choice(ERRORS), (min, max), (0, 1))
    return randint(min, max)


@command
def veryrandom(msg, min=1, max=6, base=10, num=1):
    """Los datos generados por veryrandom provienen de random.org, lo cual
    es una garantía adicional de la aleatoriedad de los resultados. Se
    obtendrá un número aleatorio entre los 2 definidos, ambos inclusive.
    """
    url = 'http://www.random.org/integers/'
    try:
        data = requests.get(url, params={
            'min': min, 'max': max, 'base': base, 'num': num,
            'col': 1, 'format': 'plain', 'rdn': 'new',
        }).text
    except Exception as e:
        data = str(e)
    return data.replace('\n', ' ')