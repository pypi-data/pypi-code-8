__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from exon.utils.command.execute import exec as run
import unittest
import sys

class RunTest(unittest.TestCase):

    def test_RunOk(self):
        out = run('/usr/bin/true')
        self.assertEqual(out.rc, 0)

    def test_RunFail(self):
        out = run('/usr/bin/false')
        self.assertEqual(out.rc, 1)

    def test_RunOutput(self):
        out = run('python %s' % __file__)
        self.assertEqual(out.stdout[0], 'Unit')
        self.assertEqual(out.stdout[1], 'Test')
        self.assertEqual(out.stderr[0], 'Unit')
        self.assertEqual(out.stderr[1], 'Test')

if __name__ == '__main__':
    print('Unit')
    print('Test')
    print('Unit', file=sys.stderr)
    print('Test', file=sys.stderr)