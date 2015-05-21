#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from __future__ import unicode_literals

from normalize_cz_unicode import normalize


# Tests =======================================================================
def test_normalize_czech_set():
    assert normalize("ařěščýřčš") == "ařěščýřčš"


def test_normalize():
    assert normalize("😭") == "?"
    assert normalize("Ǎ") == "A"

    # unbreakable and small space
    assert normalize(" ") == " "
    assert normalize(" ") == " "


def test_strange_dashes():
    assert normalize("spojovník — a ― další") == "spojovník - a - další"
