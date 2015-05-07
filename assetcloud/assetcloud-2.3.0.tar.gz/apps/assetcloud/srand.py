# -*- coding: utf-8 -*-
# (c) 2012-2013 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Cryptographically secure randomness.
"""

from bitstring import Bits
from math import log, ceil
import Crypto.Random
import string


ALPHANUMERIC_CHARS = string.letters + string.digits


def random_alphanumeric(length):
    return random_string(length, ALPHANUMERIC_CHARS)


def random_string(length, chars):
    choices = len(chars)
    bits_per_char = log(choices) / log(2)
    bits_required = length * bits_per_char
    bytes_required = bits_required / 8
    bytes_required_ceil = int(ceil(bytes_required))

    random_bytes = Crypto.Random.get_random_bytes(bytes_required_ceil)
    random_big_int = _unsigned_int_from_bytes(random_bytes)

    result = u''
    for i in xrange(length):
        (random_big_int, choice_index) = divmod(random_big_int, choices)
        chosen_char = chars[choice_index]
        result += chosen_char

    return result


def _unsigned_int_from_bytes(random_bytes):
    bits = Bits(bytes=random_bytes)
    byte_count = len(random_bytes)
    bit_count = byte_count * 8
    return bits.unpack('uint:%d' % bit_count)[0]


if __name__ == '__main__':
    print random_alphanumeric(16)
