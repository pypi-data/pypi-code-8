import fiscalmodel

from unittest import TestCase


class TestCurrency(TestCase):

    def test_currency_constant(self):
        assert fiscalmodel.CURRENCIES['EUR'] == ('Euro', True), \
            fiscalmodel.CURRENCIES['EUR']
        assert fiscalmodel.CURRENCIES['USD'] == ('US Dollar', True), \
            fiscalmodel.CURRENCIES['USD']

    def test_currency_type_raises_invalid(self):
        assert 'not-a-code' not in fiscalmodel.CURRENCIES

    def test_currency_type_returns_valid(self):
        assert 'USD' in fiscalmodel.CURRENCIES
