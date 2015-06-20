import re
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='schematec.contrib',
    packages=['schematec.contrib'],
    package_data={'': ['LICENSE']},
    version='0.1.9',
    description='Schematec contrib package',
    author='Andrey Gubarev',
    author_email='mylokin@me.com',
    url='https://github.com/mylokin/schematec.contrib',
    keywords=['schema'],
    license='MIT',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
    ),
    namespace_packages=['schematec'],
)
