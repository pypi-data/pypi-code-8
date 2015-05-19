#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from __future__ import unicode_literals

import unicodedata


# Variables ===================================================================
TRANSLATION_TABLE = {}  #: Here you can put exceptions from normalization.

_DASH_VARIANTS = "‒–—―-‐—"
TRANSLATION_TABLE.update({udash: "-" for udash in _DASH_VARIANTS})


# Functions & classes =========================================================
def _really_normalize_char(char):
    """
    Use NFKD normalization to `char`. Return ``?`` if character couldn't be
    normalized.

    Args:
        char (unicode): Unicode character which should be normalized.

    Returns:
        unicode: Normalized character.
    """
    new_char = unicodedata.normalize('NFKD', char)
    new_char = new_char.encode('ascii', errors='replace')

    # 'Ǎ' is normalized to 'A?' and I want only 'A'
    if len(new_char) == 2:
        return new_char[0]

    return new_char


def _normalize_char(char):
    """
    Use :attr:`.TRANSLATION_TABLE` to translate `char`, or
    :func:`_really_normalize_char` if `char` wasn't found in
    attr:`.TRANSLATION_TABLE`.

    Attr:
        char (unicode): Character which should be translated/normalized.

    Returns:
        unicode: Normalized character.
    """
    return TRANSLATION_TABLE.get(char, _really_normalize_char(char))


def _is_same_char(char):
    """
    Try to convert `char` to ``latin2`` encoding and compare them.

    Args:
        char (unicode): Character to test.

    Returns:
        bool: True if `char` is convertible to ``latin2`` and back.
    """
    try:
        translated = unicode(char.encode("latin2"), "latin2")
    except UnicodeEncodeError:
        return False

    return unicode(translated) == char


def normalize(inp):
    """
    Normalize `inp`. Leave only ``latin2`` acceptible characters, normalize
    everything else, using unicode `NFKD` normalization, or
    :attr:`TRANSLATION_TABLE`.

    Convert characters which couldn't be normalized to ``?``.

    Args:
        inp (unicode): Unicode string which should be normalized.

    Returns:
        unicode: Normalized string.
    """
    try:
        inp = unicode(inp)
    except UnicodeDecodeError:
        inp = unicode(inp.decode("utf-8"))

    out = u""
    for char in inp:
        if not _is_same_char(char):
            char = _normalize_char(char)

        out += char

    return out
