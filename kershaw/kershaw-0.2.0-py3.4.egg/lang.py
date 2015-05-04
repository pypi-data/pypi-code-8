from os.path import dirname
from contextlib import contextmanager
from pkgutil import iter_modules, walk_packages


@contextmanager
def ephemeral_value(obj, property_name, value, magic=True):
    """
    Runs the yielded logic with a property value temporarily set to a given value, and returns the
    value to what it was previously at completion.

    :param obj: The object to temporarily set the property value on.
    :type obj: object
    :param property_name: The name of the property to temporarily alter.
    :type property_name: str
    :param value: The value to temporarily set.
    :type value: object
    :param magic: If true (the default) use the class methods to get and set property values. If
                  false, directly call object's __getattribute__ and __setattr__ methods.
    :type magic: bool
    """
    getter, setter = (getattr, setattr) if magic else (object.__getattribute__, object.__setattr__)
    prev_property_value = getter(obj, property_name)
    setter(obj, property_name, value)
    yield
    setter(obj, property_name, prev_property_value)


def list_package_modules(package, recursive=False):
    """
    Returns a list of all of the modules available within the given package. Defaults to
    non-recursive list unless 'recursive' parameter is set to True.

    :param package: The package to get the list of modules for.
    :type package: module
    :param recursive: A flag indicating that the list method should traverse child packages of the
        specified package when generating the list, generating a list of all modules in all packages
        under the given package.
    :type recursive: bool
    :return: A list containing the names of all the packages within the package.
    :rtype: list
    """
    list_callable = iter_modules if recursive else walk_packages
    return [name for _, name, is_pkg in list_callable([dirname(package.__file__)]) if not is_pkg]


def filter_empty(target):
    """
    Remove empty items from the provided list. For the purposes of the method, an "empty" value
    is defined as any value that implements the __len__() method and has a len() value of zero.

    :param target: The list to have empty values filtered out from.
    :type target: list
    :return: The filtered list of values.
    :rtype: list
    """
    return [i for i in target if hasattr(i, '__len__') and len(i) > 0]