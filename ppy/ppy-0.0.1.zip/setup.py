"""
ppy
---

Packaging for Python.


Links
`````

* `Website <http://github.com/joeyespo/ppy>`_

"""

import os
import sys
try:
    from setuptools.command.install import install as _install
    from setuptools import setup
    from distutils.sysconfig import get_python_lib
except ImportError:
    from distutils.command.install import install as _install
    from distutils.core import setup
    from distutils.sysconfig import get_python_lib


if sys.argv[-1] == 'publish':
    sys.exit(os.system('python setup.py sdist upload'))


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


def _postinstall(instance, install_lib):
    # TODO: Do anything here?
    pass


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_postinstall, (self, self.install_lib,),
                     msg='Running postinstall')


# TODO: Post-install script to install requirements.json dependencies?


setup(
    name='ppy',
    version='0.0.1',
    description='Packaging for Python.',
    long_description=__doc__,
    author='Joe Esposito',
    author_email='joe@joeyespo.com',
    url='http://github.com/joeyespo/ppy',
    license='MIT',
    platforms='any',
    packages=['ppy'],
    package_data={'': ['LICENSE']},
    # TODO: Only install the import hook if installing ppy globally
    data_files=[(get_python_lib(), ['ppy_import_hook.pth'])],
    install_requires=read('requirements.txt').splitlines(),
    entry_points={'console_scripts': ['ppy = ppy.cli:main']},
    cmdclass={'install': install},
)
