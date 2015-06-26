
# -*- coding: utf-8 -*-

"""
Function composition is simple, just use funcomp.
Copyright (C) 2015, Bence Faludi (bence@ozmo.hu)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, <see http://www.gnu.org/licenses/>.
"""

import unittest
from funcomp import Composition, absorb, NotCallable

class TestEmptyComposition(unittest.TestCase):
    def test_without_function(self):
        comp = Composition()
        self.assertIsNone(comp())
        self.assertEqual(comp(10), 10)
        self.assertEqual(comp('Monkey'), 'Monkey')

class TestSingleFunctionComposition(unittest.TestCase):
    def _myfunc(self, value):
        return (value%2)+1

    @staticmethod
    def _mystaticfunc(value):
        return value-10

    @classmethod
    def _myclassfunc(cls, value):
        return value+7

    def test_static_method_success(self):
        comp = Composition(TestSingleFunctionComposition._mystaticfunc)
        self.assertEqual(comp(11), 1)

    def test_class_method_success(self):
        comp = Composition(TestSingleFunctionComposition._myclassfunc)
        self.assertEqual(comp(11), 18)

    def test_static_method_error(self):
        comp = Composition(TestSingleFunctionComposition._mystaticfunc)
        with self.assertRaises(TypeError):
            comp('11')

        comp = Composition(absorb(TestSingleFunctionComposition._mystaticfunc))
        self.assertIsNone(comp('11'))

    def test_class_method_error(self):
        comp = Composition(TestSingleFunctionComposition._myclassfunc)
        with self.assertRaises(TypeError):
            comp('11')

        comp = Composition(absorb(TestSingleFunctionComposition._myclassfunc))
        self.assertIsNone(comp('11'))

    def test_not_function(self):
        with self.assertRaises(NotCallable):
            Composition('_not_a_function')

    def test_multiple_paramter_number(self):
        def myfunc(value, mod = 2):
            return (value%mod)+1

        comp = Composition(myfunc)
        self.assertEqual(comp(9), 2)

        # Only one parameter is allowed!
        with self.assertRaises(TypeError):
            comp(9,3)

    def test_builtin_function_success(self):
        comp = Composition(str.strip)
        self.assertEqual(comp('  Monkey '), 'Monkey')

    def test_builtin_function_error(self):
        comp = Composition(str.strip)
        with self.assertRaises(TypeError):
            comp()

        with self.assertRaises(TypeError):
            comp(18.8)

        comp = Composition(absorb(str.strip))
        self.assertIsNone(comp())
        self.assertIsNone(comp(18.8))

    def test_function_success(self):
        def myfunc(value):
            return (value%2)+1

        comp = Composition(myfunc)
        self.assertEqual(comp(9), 2)

    def test_function_error(self):
        def myfunc(value):
            return (value%2)+1

        comp = Composition(myfunc)
        with self.assertRaises(TypeError):
            comp('Pillow')

        comp = Composition(absorb(myfunc))
        self.assertIsNone(comp('Pillow'))

    def test_bound_method_success(self):
        comp = Composition(self._myfunc)
        self.assertEqual(comp(9), 2)

    def test_bound_method_error(self):
        comp = Composition(self._myfunc)
        with self.assertRaises(TypeError):
            comp('Pillow')

        comp = Composition(absorb(self._myfunc))
        self.assertIsNone(comp('Pillow'))

class TestMultipleFunctionComposition(unittest.TestCase):
    def _myfunc(self, value):
        return (value%2)+1

    @staticmethod
    def _mystaticfunc(value):
        return value-10

    @classmethod
    def _myclassfunc(cls, value):
        return value+7

    def test_not_function(self):
        def myfunc(value):
            return value.replace('a','')

        with self.assertRaises(NotCallable):
            Composition(str, str.strip, str.lower, 9.1, myfunc, len, self._myfunc)

    def test_mixed_function_success(self):
        def myfunc(value):
            return value.replace('a','')

        comp = Composition(str, str.strip, str.lower, myfunc, len, self._myfunc, \
             TestMultipleFunctionComposition._mystaticfunc, \
             TestMultipleFunctionComposition._myclassfunc)

        self.assertEqual(comp(), -2)
        self.assertEqual(comp('  avoCADdO '), -2)

    def test_mixed_function_error(self):
        def myfunc(value):
            return value.replace('a','')

        comp = Composition(str.strip, str.lower, myfunc, len, self._myfunc)
        with self.assertRaises(TypeError):
            comp(7)

        acomp = Composition(absorb(comp))
        self.assertIsNone(acomp(7))

        acomp = Composition(absorb(comp, use_original=True))
        self.assertEqual(acomp(7), 7)

class TestAbsorb(unittest.TestCase):
    def test_builtin_function_success(self):
        self.assertEqual(absorb(str.strip)(' FunComp '), 'FunComp')

    def test_type_success(self):
        self.assertEqual(absorb(int)(' 7 '), 7)

    def test_function_success(self):
        def myfunc(value):
            return (value%2)+1

        self.assertEqual(absorb(myfunc)(9), 2)

    def test_absorb_error_to_none(self):
        self.assertEqual(absorb(int)(' Banana'), None)

    def test_absorb_error_use_original(self):
        self.assertEqual(absorb(int, use_original=True)(' Banana'), ' Banana')

    def test_multiple_paramter_number(self):
        def myfunc(value, mod = 2):
            return (value%mod)+1

        self.assertEqual(absorb(myfunc)(9,3), 1)

    def test_wrong_parameter_number(self):
        def myfunc():
            return 9

        self.assertEqual(absorb(myfunc)(7), None)
        with self.assertRaises(TypeError):
            absorb(myfunc)()

    def test_none_function(self):
        with self.assertRaises(NotCallable):
            absorb(None)(' FunComp ')

    def test_not_function(self):
        with self.assertRaises(NotCallable):
            absorb('anystring')(' FunComp ')
