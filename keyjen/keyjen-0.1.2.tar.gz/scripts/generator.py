#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    It generates plenty of keys with different length and count. You can create random passwords, client_keys or secrets

    Author: Uğur Soğukpınar
    Date: 1 July 2015
    Python Version: 3.4.3
"""

import random


class Generator(object):
    VERSION = '0.1.2'  # Versiyon bilgilendirmelerini buradan çekerek yapacağız.

    __uppers = ['A', 'B', 'C', 'D', 'E', 'F', 'Z', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'X']
    __digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    __lowers = [letter.lower() for letter in __uppers]

    __chars = {
        'upper': __uppers,
        'digit': __digits,
        'lower': __lowers,
    }

    def __init__(self, length, types, count, **kwargs):
        """
        :param length: Integer
        :param types: List
        :param count: Integer
        :return: void
        """

        self.length = int(length)
        self.types = types
        self.count = int(count)
        self.char_pool = []
        self.prepare_types()
        self.prefix = ''
        self.suffix = ''

        if kwargs.get('prefix', None) is not None:
            self.prefix = kwargs['prefix']

        if kwargs.get('suffix', None) is not None:
            self.suffix = kwargs['suffix']

        self.prepare_prefix()
        self.prepare_suffix()
        self.generated_keys = []
        self.run()

    def run(self):
        for i in range(self.count):
            self.generated_keys.append(self.generate_key())

    def prepare_types(self):
        """
        :return: void
        :raises: TypeError
        """
        types_can_be = ('lower', 'upper', 'digit', 'all')

        if not all(v in types_can_be for v in self.types):
            raise TypeError(u"Unexpected type value")

        if 'all' in self.types:
            for v in self.__chars:
                self.char_pool += self.__chars[v]
        else:
            for v in self.types:
                self.char_pool += self.__chars[v]

    def prepare_suffix(self):
        if len(self.suffix):
            if self.length > len(self.suffix):
                self.length -= len(self.suffix)
            else:
                raise Exception("Suffix cannot be longer than key length")

    def prepare_prefix(self):
        if len(self.prefix):
            if self.length > len(self.prefix):
                self.length -= len(self.prefix)
            else:
                raise Exception("Prefix cannot be longer than key length")

    def generate_key(self):
        """
        Ayarlanan karakter tiplerine göre bir adet key üretir.
        :return: String
        """
        key_str = self.prefix

        for i in range(self.length):
            key_str += random.choice(self.char_pool)

        key_str += self.suffix
        return key_str

    def print_keys(self):
        for key in self.generated_keys:
            print(key)