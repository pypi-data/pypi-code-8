#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from kwargs_obj import KwargsObj


# Classes =====================================================================
class KWTest(KwargsObj):
    def __init__(self, **kwargs):
        self.some_attr = None
        self.something = None

        self._kwargs_to_attributes(kwargs)


class DisableSettingAttributes(KwargsObj):
    def __init__(self):
        self.something = None

        self._all_set = True


# Tests =======================================================================
def test_blank_constructor():
    k = KWTest()

    assert k


def test_attribute_mapping():
    k = KWTest(
        some_attr=True
    )

    assert k.some_attr
    assert not k.something

    k.something = True
    assert k.something


def test_both_attributes():
    k = KWTest(
        some_attr=True,
        something=True
    )

    assert k.some_attr
    assert k.something


def test_invalid_attributes():
    with pytest.raises(ValueError):
        KWTest(azgabash=True)

    with pytest.raises(ValueError):
        KWTest(
            some_attr=True,
            azgabash=True
        )


def test_disable_setting():
    k = KWTest()

    # test setting nonexistent attribute
    k.azgabash = True
    assert hasattr(k, "azgabash")

    d = DisableSettingAttributes()

    with pytest.raises(ValueError):
        d.azgabash = True

    # you should be able to define existing attributes
    d.something = False
