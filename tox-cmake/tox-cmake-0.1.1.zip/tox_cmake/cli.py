# -*- coding: utf-8 -*-


import fnmatch
import itertools
import os.path
import subprocess
import sys
try:
    import winreg
except ImportError:
    import _winreg as winreg


def _version_eq(constraint, version):
    version = version.split('-')[0]
    version = map(int, version.split('.'))
    if len(constraint) != len(version):
        return False
    for c, v in zip(constraint, version):
        if v != c:
            return False
    # TODO: allow trailing zeros.
    return True


def _version_ge(constraint, version):
    version = version.split('-')[0]
    version = map(int, version.split('.'))
    if version[0] != constraint[0]:
        return False
    for c, v in zip(constraint[1:], version[1:]):
        if v < c:
            return False
    return True


def _version_lt(constraint, version):
    version = version.split('-')[0]
    version = map(int, version.split('.'))
    for i in range(len(constraint)):
        if version[i] < constraint[i]:
            return True
    return False


def _version_tagged(constraint, version):
    try:
        version = version.split('-')[1]
    except IndexError:
        return False
    return fnmatch.fnmatch(constraint, version)


def _compile_constraint(constraint):
    if constraint.startswith('=='):
        constraint = map(int, constraint[2:].split('.'))
        return lambda v: _version_eq(constraint, v)
    if constraint.startswith('>='):
        constraint = map(int, constraint[2:].split('.'))
        return lambda v: _version_ge(constraint, v)
    if constraint.startswith('<'):
        constraint = map(int, constraint[1:].split('.'))
        return lambda v: _version_lt(constraint, v)
    if constraint.startswith('-'):
        constraint = constraint[1:]
        return lambda v: _version_tagged(constraint, v)
    raise ValueError('Invalid constraint "%s".' % constraint)


def select_version(pattern, versions):
    constraints = map(_compile_constraint, pattern.split(','))
    for version in versions:
        if all(c(version) for c in constraints):
            return version
    return None


def main(arguments=None):
    if arguments is None:
        arguments = sys.argv[1:]
    with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as root:
        # Enumerate Kitware products to find installed CMake versions.
        versions = []
        with winreg.OpenKey(root, 'SOFTWARE\\Kitware') as key:
            for i in itertools.count():
                try:
                    product = winreg.EnumKey(key, i)
                    if product.startswith('CMake'):
                        versions.append(product.split(' ', 1)[1])
                except WindowsError as error:
                    if error.errno != 22:
                        raise
                    break

        # Select a version that matches the desired constraints.
        version = select_version(arguments[0], versions)
        if not version:
            sys.stderr.write(
                'No installed CMake version matches "%s".' % arguments[0]
            )
            return 2

        # Find the path to the selected version.
        try:
            path = 'SOFTWARE\\Kitware\\CMake ' + version
            with winreg.OpenKey(root, path) as key:
                cmake_path = winreg.QueryValue(key, '')
        except WindowsError as error:
            if error.errno != 2:
                raise
            sys.stderr.write('CMake "%s" not installed.' % version)
            return 1

    # Call CMake.
    return subprocess.call(
        [os.path.join(cmake_path, 'bin', 'cmake.exe')] + arguments[1:]
    )


if __name__ == '__main__':
    sys.exit(main())
