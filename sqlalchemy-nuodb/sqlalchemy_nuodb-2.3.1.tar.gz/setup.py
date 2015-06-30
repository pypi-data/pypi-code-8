import os
import re

from setuptools import setup

v = open(os.path.join(os.path.dirname(__file__), 'sqlalchemy_nuodb', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()
print(VERSION)
readme = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='sqlalchemy_nuodb',
    version=VERSION,
    description="SQLAlchemy for NuoDB",
    long_description=open(readme).read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Database :: Front-Ends',
    ],
    keywords='SQLAlchemy NuoDB',
    author='Robert Buck',
    author_email='buck.robert.j@gmail.com',
    license='MIT',
    packages=['sqlalchemy_nuodb'],
    include_package_data=True,
    tests_require=['nose >= 0.11', 'mock'],
    test_suite="nose.collector",
    zip_safe=False,
    install_requires=['sqlalchemy>=1.0.4'],
    entry_points={
        'sqlalchemy.dialects': [
            'nuodb = sqlalchemy_nuodb.pynuodb:NuoDBDialect_pynuodb',
            'nuodb.pynuodb = sqlalchemy_nuodb.pynuodb:NuoDBDialect_pynuodb',
        ]
    }
)
