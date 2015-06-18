# Filename: monkeypatch_test.py
import unittest
import monkeypatch as mp


@mp.monkeypatch
class Example(object):

    def __init__(self, val=0):
        self.val = val

    @mp.route('raise_([0-9]+).to_([0-9]+).power')
    def power(self, a, b):
        a = int(a)
        b = int(b)
        return a ** b + self.val

    def mul(self, a, b):
        return a * b


@mp.monkeypatch
class NestedExample(Example):

    def __init__(self, depth=0, val=0):
        super(Example, self).__init__(val)
        if depth:
            self.ptr = NestedExample(depth - 1, val * 2)

    @mp.route('invert_([0-9]+)')
    def inv(self, num):
        return self.val + 1.0 / int(num)


class TestMonkeyPatch(unittest.TestCase):

    def testBasicRoute(self):
        a = Example()
        self.assertEqual(a.raise_2.to_5.power(), 32)

    def testDecoratedOriginal(self):
        a = Example()
        self.assertEqual(a.power(2, 5), 32)

    def testUndecorated(self):
        a = Example()
        self.assertEqual(a.mul(2, 5), 10)

    def testCtor(self):
        a = Example(5)
        self.assertEqual(a.raise_2.to_5.power(), 37)
        self.assertEqual(a.power(2, 5), 37)
        self.assertEqual(a.mul(2, 5), 10)


class TestNestedMonkeyPatch(unittest.TestCase):

    def testCtor(self):
        a = NestedExample(5, 5)
        for i in range(5):
            self.assertAlmostEqual(a.invert_2(), 5 * (2**i) + 0.5)
            self.assertAlmostEqual(a.inv(2), 5 * (2**i) + 0.5)
            self.assertEqual(a.power(2, 5), 32 + 5 * (2 ** i))
            self.assertEqual(a.raise_2.to_5.power(), 32 + 5 * (2 ** i))
            a = a.ptr


if __name__ == '__main__':
    unittest.main()
