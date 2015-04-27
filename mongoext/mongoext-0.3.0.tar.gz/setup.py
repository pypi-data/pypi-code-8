import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = ''

with open('mongoext/__init__.py', 'r') as fd:
    regex = re.compile(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]')
    for line in fd:
        m = regex.match(line)
        if m:
            version = m.group(1)
            break

setup(
    name='mongoext',
    packages=['mongoext'],
    package_data={'': ['LICENSE']},
    install_requires=['pymongo==3.0'],
    version=version,
    description='Data models for Mongo',
    author='Andrey Gubarev',
    author_email='mylokin@me.com',
    url='https://github.com/mylokin/mongoext',
    keywords=['mongodb', 'orm', 'models'],
    license='MIT',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
    ),
)
