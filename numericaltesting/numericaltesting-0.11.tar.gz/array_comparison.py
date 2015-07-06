import numpy as np


def spy(a, t=1e-5):
    """
    Return a string representation of the sparsity pattern of A.
    """
    a = np.atleast_2d(a)
    return '\n'.join(map(lambda row: '['+''.join(np.where(np.abs(row) > t, 'x', ' '))+']', a))


def assert_same_shape(x, y):
    """
    Assert that x and y have the same shape
    """
    xh = np.shape(x)
    yh = np.shape(y)
    assert xh == yh, "Shape mismatch: %s vs %s" % ("x".join(map(str, xh)), "x".join(map(str, yh)))    


def assert_no_errors(errors, x, y, msg, linelimit=20, xlabel='LHS', ylabel='RHS'):
    """
    Check errors contains only false.
    If they are not then print some helpful diagnostic information and raise an AssertionError.
    """
    if np.any(errors):
        error_coords = list(zip(*np.nonzero(errors)))
        for coord in error_coords[:linelimit]:
            print("coord:", coord)
            print('Error at position %s: %s=%s vs %s=%s' % (','.join(map(str, coord)), xlabel, x[coord], ylabel, y[coord]))
        if len(error_coords) > linelimit:
            print('... and %d more' % (len(error_coords) - linelimit))
        if x.ndim > 1 and np.prod(x.shape) > 10:
            print('\n' + xlabel + ':')
            print(spy(x))
            print('\n' + ylabel + ':')
            print(spy(y))
            print('\nError:')
            print(spy(errors))
        else:
            print('\n:' + xlabel + ':')
            print(x)
            print('\n' + ylabel + ':')
            print(y)
            print('\nSparsity pattern of error:')
            print(spy(errors))
        raise AssertionError(msg)


def assert_arrays_equal(x, y, decimals=6, **kwargs):
    """
    Check that x and y are equal to within the specified number of decimal places.
    If they are not then print some helpful diagnostic information and raise an AssertionError.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    assert_same_shape(x, y)
    errors = x != y
    msg = "arrays were not identical"
    assert_no_errors(errors, x, y, msg, **kwargs)


def assert_arrays_almost_equal(x, y, decimals=6, **kwargs):
    """
    Check that x and y are identical.
    If they are not then print some helpful diagnostic information and raise an AssertionError.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    assert_same_shape(x, y)
    tol = np.maximum(10**-decimals, np.abs(np.maximum(x, y) * 10**-decimals))
    errors = np.abs(x - y) > tol
    msg = "arrays were not equal to %d decimals" % decimals
    assert_no_errors(errors, x, y, msg, **kwargs)
