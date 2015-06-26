# Copyright (c) Moshe Zadka
# See LICENSE for details.

"""mainland -- a main for Python"""

from mainland._version import get_versions as _get_versions

__version__ = _get_versions()['version']

_long_description = '''\
mainland_: A way to run Python scripts without console-scripts

.. _mainland: https://mainland.rtfd.org
'''

metadata = dict(
    name='mainland',
    description='Run your modules',
    long_description=_long_description,
    author='Moshe Zadka',
    author_email='zadka.moshe@gmail.com',
    license='MIT',
    copyright='2015',
)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from mainland._main import main

main = main
