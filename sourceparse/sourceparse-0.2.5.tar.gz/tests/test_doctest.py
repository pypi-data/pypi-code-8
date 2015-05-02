import doctest


def test_doctests():
    doctest.testfile('../README.rst')


if __name__ == '__main__':
    test_doctests()
