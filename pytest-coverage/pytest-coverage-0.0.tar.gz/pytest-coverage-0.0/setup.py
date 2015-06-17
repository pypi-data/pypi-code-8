# encoding: utf8

from setuptools import setup

setup(
    name='pytest-coverage',
    version="0.0",
    url='https://pypi.python.org/pypi/pytest-cover/',
    description='Pytest plugin for measuring coverage. Forked from `pytest-cov`.',
    long_description='''Use `pytest-cover <https://pypi.python.org/pypi/pytest-cover/>`_ instead.''',
    author='Marc Schlaich',
    platforms=['all'],
    zip_safe=False,
    author_email='marc.schlaich@gmail.com',
    install_requires=['pytest-cover'],
)
