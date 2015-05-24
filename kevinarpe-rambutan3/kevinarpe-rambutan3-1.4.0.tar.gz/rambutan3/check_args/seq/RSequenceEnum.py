import enum
from _collections_abc import Sequence, MutableSequence

from rambutan3.enumeration.REnum import REnum


@enum.unique
class RSequenceEnum(REnum):

    TUPLE = (tuple,)
    LIST = (list,)
    SEQUENCE = (tuple, Sequence, list, MutableSequence)
