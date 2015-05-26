import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = ''

with open('schematec/__init__.py', 'r') as fd:
    regex = re.compile(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]')
    for line in fd:
        m = regex.match(line)
        if m:
            version = m.group(1)
            break

setup(
    name='schematec',
    packages=['schematec'],
    package_data={'': ['LICENSE']},
    version=version,
    description='Set of tools that makes input data validation easier',
    author='Andrey Gubarev',
    author_email='mylokin@me.com',
    url='https://github.com/mylokin/schematec',
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
)
