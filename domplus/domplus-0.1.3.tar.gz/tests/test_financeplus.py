# -*- coding: utf-8 -*-
from nose.tools import assert_equal
from domplus import financeplus


def test_is_valid_creditcard():
    """
    Test is_valid_creditcard
    """
    # True
    assert_equal(True, financeplus.is_valid_creditcard('376226864104614'))  # Amex
    assert_equal(True, financeplus.is_valid_creditcard('6762498687801564'))  # Maestro
    assert_equal(True, financeplus.is_valid_creditcard('4021087370711545'))  # Visa
    assert_equal(True, financeplus.is_valid_creditcard('5480450562290085'))  # Mastercard
    assert_equal(True, financeplus.is_valid_creditcard('3095734612723704'))  # Diners Club
    assert_equal(True, financeplus.is_valid_creditcard('5078601870000127985'))  # Aura
    assert_equal(True, financeplus.is_valid_creditcard('6011111111111117'))  # Discover
    assert_equal(True, financeplus.is_valid_creditcard('6362970000457013'))  # Elo
    assert_equal(True, financeplus.is_valid_creditcard('6062825624254001'))  # Hipercard
    assert_equal(True, financeplus.is_valid_creditcard('3530111333300000'))  # JCB
    assert_equal(True, financeplus.is_valid_creditcard('50339619890917'))  # Maestro

    # False
    assert_equal(False, financeplus.is_valid_creditcard('376226864104610'))  # Amex
    assert_equal(False, financeplus.is_valid_creditcard('6762498687801560'))  # Maestro
    assert_equal(False, financeplus.is_valid_creditcard('4021087370711540'))  # Visa
    assert_equal(False, financeplus.is_valid_creditcard('5480450562290080'))  # Mastercard
    assert_equal(False, financeplus.is_valid_creditcard('3095734612723700'))  # Diners Club
    assert_equal(False, financeplus.is_valid_creditcard('5078601870000127980'))  # Aura
    assert_equal(False, financeplus.is_valid_creditcard('6011111111111110'))  # Discover
    assert_equal(False, financeplus.is_valid_creditcard('6362970000457010'))  # Elo
    assert_equal(False, financeplus.is_valid_creditcard('6062825624254000'))  # Hipercard
    assert_equal(False, financeplus.is_valid_creditcard('3530111333000000'))  # JCB
    assert_equal(False, financeplus.is_valid_creditcard('50339619890910'))  # Maestro
