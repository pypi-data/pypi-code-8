"""
setup.py
========

:copyright: (c) 2015 by Yi-Xin Liu
:license: BSD, see LICENSE.txt for more details.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os

cwd = os.path.dirname(os.path.abspath(__file__))

# Read __version__ from _version.py and add it into the current variable space.
exec(open('pydiagram/_version.py').read())

setup(
    name='pydiagram',
    version=__version__,  # NOQA
    license='BSD',
    description='PyDiagram is a python package for generating a phase diagram from results output by polymer field-theoretic simulations. PyDiagram also provides functions for analysis of simulation results.',
    author='Yi-Xin Liu',
    author_email='liuyxpp@gmail.com',
    url='https://github.com/liuyxpp/pydiagram',
    packages=['pydiagram'],
    include_package_data=True,
    entry_points={
        "console_scripts": ['pydiagram = pydiagram.__main__:main']
    },
    zip_safe=False,
    long_description=open(os.path.join(cwd, 'README.rst')).read(),
    install_requires=[
        'mpltex>=0.3',
        'matplotlib',
        'numpy',
        'scipy',
        'attrdict>=2.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
