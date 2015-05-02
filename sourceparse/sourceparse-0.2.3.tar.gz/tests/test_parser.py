""" main test module """
import os
import unittest
from sourceparse import CodeCollector


class TestParser(unittest.TestCase):

    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'lorem.py')
        self.parser = CodeCollector(filename)

    def testClasses(self):
        """ we find classes name
        """
        got = [c.name for c in self.parser.classes]
        expected = ['Base', 'Sub1', 'MixinUser']
        self.assertEquals(got, expected)

    def testClassesLines(self):
        """ we find classes lines
        """
        got = [(c.from_line, c.to_line) for c in self.parser.classes]
        expected = [(3, 12), (13, 17), (18, 36)]
        self.assertEquals(got, expected)

    def testClassesDecorators(self):
        """ we find classes decorators
        """
        got = [c.decorators for c in self.parser.classes]
        expected = [['@decorated(somehow)\n', '@extra\n'], [], []]
        self.assertEquals(got, expected)

    def testClassesDocstrings(self):
        """ we find classes docstrings
        """
        got = [c.docstring for c in self.parser.classes]
        expected = ['This is the base class.\n    ',
                    'This is the first subclass.\n    ',
                    'Overrides method1 and method2\n    ']
        self.assertEquals(got, expected)

    def testClassesMethods(self):
        """ we find classes methods
        """
        got = [m.name for c in self.parser.classes for m in c.methods]
        expected = ['method1', 'method1', 'method2']
        self.assertEquals(got, expected)

    def testClassesMethodsDocstrings(self):
        """ we find classes methods docstrings
        """
        classes_methods = [c.methods for c in self.parser.classes]
        got = [m.docstring for cm in classes_methods for m in cm]
        expected = ['method1 of Base\n    ',
                    'method1 of MixinUser\n    ',
                    'method2 of MixinUser\n    ']
        self.assertEquals(got, expected)

    def testClassesMethodsArgs(self):
        """ we find classes methods args
        """
        classes_methods = [c.methods for c in self.parser.classes]
        got = [m.args for cm in classes_methods for m in cm]
        expected = [[], ['foo', 'bar'], ['foo']]
        self.assertEquals(got, expected)

    def testClassesMethodsKWArgs(self):
        """ we find classes methods kwargs
        """
        classes_methods = [c.methods for c in self.parser.classes]
        got = [m.kwargs for cm in classes_methods for m in cm]
        expected = [{}, {}, {'baz': 'None'}]
        self.assertEquals(got, expected)

    def testClassesMethodsLines(self):
        """ we find classes methods lines
        """
        classes_methods = [c.methods for c in self.parser.classes]
        got = [(m.from_line, m.to_line) for cm in classes_methods for m in cm]
        expected = [(7, 12), (22, 26), (29, 36)]
        self.assertEquals(got, expected)

    def testFunctions(self):
        """ we find module functions name
        """
        got = [f.name for f in self.parser.functions]
        expected = ['my_function', 'my_decorated_function']
        self.assertEquals(got, expected)

    def testFunctionsLines(self):
        """ we find functions lines
        """
        got = [(f.from_line, f.to_line) for f in self.parser.functions]
        expected = [(37, 42), (44, 47)]
        self.assertEquals(got, expected)

    def testFunctionsDecorators(self):
        """ we find functions decorators
        """
        got = [f.decorators for f in self.parser.functions]
        expected = [[], ['@deprecated\n']]
        self.assertEquals(got, expected)

    def testFunctionsDocstrings(self):
        """ we find functions docstrings
        """
        got = [f.docstring for f in self.parser.functions]
        expected = ['Stand-alone function.\n    ',
                    'Another stand-alone function.\n    ']
        self.assertEquals(got, expected)

    def testFunctionsArgs(self):
        """ we find functions args
        """
        got = [f.args for f in self.parser.functions]
        expected = [['foo'], ['foo', 'bar']]
        self.assertEquals(got, expected)
