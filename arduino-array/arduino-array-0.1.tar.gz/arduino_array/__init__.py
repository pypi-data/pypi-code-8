import os


def get_includes():
    import arduino_array
    r"""
    Return the directory that contains the `arduino_array` Cython *.hpp and
    *.pxd header files.

    Extension modules that need to compile against `arduino_array` should use
    this function to locate the appropriate include directory.

    Notes
    -----
    When using ``distutils``, for example in ``setup.py``.
    ::

        import arduino_array
        ...
        Extension('extension_name', ...
                  include_dirs=[...] + arduino_array.get_includes())
        ...

    """
    return [os.path.join(os.path.dirname(arduino_array.__file__), 'Arduino',
                         'Array')]
