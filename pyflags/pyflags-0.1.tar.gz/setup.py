try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name='pyflags',
    version='0.1',
    description='A simple, common-sense, single-letter command-line parser',
    author='Ryan Gonzalez',
    py_modules=['flags'],
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ])
