#!/usr/bin/python
# -*- coding: utf-8 -*-

from bitstring import BitArray

from .binary import bits_to_group
# from .permutation import permute  # not neeed for now but might be in future
from .rearrange import re_arrange, reverse_order


class Scrambler(object):
    """
    Scrambler is the base class for creating different scrambling systems
    using this module.
    """
    def __init__(self, trans, keys):
        """
        Where trans is one int or an array of ints specifying the length in
        bits of chunks that the input data bytearray should be divided into.
        If an array is passed then scrambling will scramble once for every int
        in the array for the given size of each item.

        keys should be an array of bytearrays or equivalent data strutctures
        that will be used for scrambling the data.
        """
        if isinstance(trans, int):
            self.trans = [trans]
        elif hasattr(trans, '__iter__'):
            self.trans = trans
        else:
            raise TypeError('Non iterable or int type passed as trans arg.')
        if isinstance(keys, list):
            self.keys = self.keygen(keys)
        else:
            raise TypeError('Non-iterable or bytes type passed as keys arg.')

    def keygen(self, keys):
        """
        This method is used to generate the keys for this scramble object based
        on the input keys array. By default it just assumes that these arrays
        contain the order transform to be applied (i.e. an array of
        non-repeating ints each corresponding to a position in said array).
        """
        return keys

    def key_getter(self, n):
        """
        The key_getter method can be overridden to change how keys are selected
        when multiple trans and/or keys are given. By default, it is assumed
        both of these contain the same number of items and Exceptions will be
        thrown if not the case.
        """
        return self.keys[n]

    def scramble(self, data):
        """
        Scramble input data, returning the scrambled copy.
        For every item in trans array, transform data bytes to this bit width
        then apply the rearrange function.
        """
        if isinstance(data, BitArray):
            scrambled = BitArray(data)
        else:
            scrambled = BitArray(bytearray(data))
        size = len(scrambled)
        for index, width in enumerate(self.trans):
            # get key for this turn:
            key = self.key_getter(index)
            # split up to chunks of given bit width:
            chunks = bits_to_group(scrambled, width)
            # re-arrange the array of bitarrays:
            jumbled = re_arrange(chunks, key)
            # convert to one whole bitarray again:
            scram = bits_to_group(jumbled, size)
            # assign to scrambled - there should only be one item in array
            scrambled = scram[0]
        return scrambled

    def unscramble(self, data):
        if isinstance(data, BitArray):
            unscrambled = BitArray(data)
        else:
            unscrambled = BitArray(bytearray(data))
        size = len(unscrambled)
        # working backwards both for the keys and the transforms:
        for index, width in reversed(list(enumerate(self.trans))):
            # get key for this turn (get the inverse of it)
            key = reverse_order(self.key_getter(index))
            # split up to chunks of given bit width:
            chunks = bits_to_group(unscrambled, width)
            # re-arrange the array of bitarrays:
            jumbled = re_arrange(chunks, key)
            # convert to one whole bitarray again:
            uscram = bits_to_group(jumbled, size)
            # assign to unscrambled - there should only be one item in array
            unscrambled = uscram[0]
        return unscrambled
