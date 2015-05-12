'''
object_by_name
==============
Get an object by name or dotted path, import if it necessary.

Install
-------
    pip install object_by_name

Usage
-----
    >>> from object_by_name import object_by_name

    >>> object_by_name('test_package')
    <module 'test_package' from ...>

    >>> object_by_name('test_package.test_module')
    <module 'test_package.test_module' from ...>

    >>> object_by_name('test_package.test_module.TestClass')
    <class 'test_package.test_module.TestClass'>

    >>> object_by_name('test_package.test_module.instance')
    <test_package.test_module.TestClass object at 0x...>

    >>> object_by_name('test_package.test_module.instance.method')
    <bound method TestClass.method of <test_package.test_module.TestClass ...>>
'''
import sys

if sys.version_info > (3, ):
    basestring = str


def object_by_name(name):
    if not isinstance(name, basestring):
        return name

    if '.' not in name:
        return __import__(name)

    parts, attrs = name.split('.'), []
    while parts:
        module = '.'.join(parts)
        try:
            obj = __import__(module, {}, {}, [''])
        except ImportError:
            attrs.insert(0, parts.pop())
            continue
        for attr in attrs:
            try:
                obj = getattr(obj, attr)
            except AttributeError:
                raise ImportError('could not import "%s": "%s" doesn\'t have'
                                  ' attribute "%s"' % (name, module, attr))
        return obj
    raise ImportError('could not import "%s"' % name)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True, raise_on_error=True,
                    optionflags=doctest.ELLIPSIS)
