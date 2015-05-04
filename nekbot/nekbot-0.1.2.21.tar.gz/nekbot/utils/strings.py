# coding=utf-8
import shlex
import re
from nekbot.utils.ints import get_int

__author__ = 'nekmo'



def long_message(message, newlines=1, length=140):
    if not isinstance(message, (str, unicode)):
        message = str(message)
    if len(message) > length:
        return True
    if len(message.split('\n')) - 1 > newlines:
        return True
    return False


def split_arguments(body):
    """Dividir una cadena de texto en un listado de argumentos como en un shell.
    """
    # Sustituyo todas las comillas sencillas entre palabras por car \x00 para luego
    # devolverlo a su original. Hago esto, porque seguramente sea un apóstrofe como
    # los usados en inglés.
    body = re.sub(r"([^\A ])\'([^\Z ])", "\\1\x00\\2", body)
    args = shlex.split(body)
    args = map(lambda x: x.replace('\x00', "'"), args)
    return args


def find_occurrences(key, text):
    return map(lambda x: x.start(), re.finditer(re.escape(key), text))


def limit_context(key, text, chars_context=10, limiter='[...]'):
    results = []
    for occurrence in find_occurrences(key, text):
        part_a = text[get_int(occurrence - chars_context, 0):occurrence]
        part_b = text[occurrence + len(key):get_int(occurrence + len(key) + chars_context, len(text))]
        results.append('{limiter}%s{key}%s{limiter}'.format(**locals()) % (part_a, part_b))
    return ' '.join(results)


def highlight_occurrence(text, occurrence, char='*'):
    return re.sub('(%s)' % re.escape(occurrence), r'{char}\1{char}'.format(char=char), text)