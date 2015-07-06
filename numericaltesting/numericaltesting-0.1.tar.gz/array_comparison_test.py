import unittest
import numpy as np

from .array_comparison import assert_arrays_almost_equal, assert_arrays_equal


class ArrayComparisonTest(unittest.TestCase):
	def test_arrays_almost_equal(self):
		a = [1, 2, 3]
		with self.assertRaises(AssertionError):
			assert_arrays_almost_equal(a, [0, 0, 0])

		# Should not raise an error:
		assert_arrays_almost_equal(a, [1, 2, 3])

		# Should not raise an error:
		assert_arrays_almost_equal(a, [1.01, 2.01, 3.01], decimals=1)

	def test_arrays_almost_equal(self):
		a = [1, 2, 3]
		with self.assertRaises(AssertionError):
			assert_arrays_equal(a, [0, 0, 0])
		assert_arrays_equal(a, [1, 2, 3])


if __name__ == '__main__':
	unittest.main()
