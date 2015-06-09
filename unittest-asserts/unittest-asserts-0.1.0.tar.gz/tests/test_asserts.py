from nose.tools import assert_raises
from asserts import sparse_check


def test_sparse_check():
    sparse_check({'status': 'ok'},
                 {'status': 'ok', 'results': [1, 2, 3]})

    assert_raises(AssertionError,
                  sparse_check,
                  {'status': 'ok'},
                  {'status': 'error', 'results': [1, 2, 3]})


def test_sparse_simple_lists():
    sparse_check(['One', 'Two', 'Tree'],
                 ['One', 'Two', 'Tree'])

    assert_raises(AssertionError,
                  sparse_check,
                  ['One', 'Two', 'Tree'],
                  ['One', 'Tree', 'Two'])
