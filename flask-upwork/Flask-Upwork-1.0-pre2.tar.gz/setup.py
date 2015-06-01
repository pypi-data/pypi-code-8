"""
Flask-Upwork
-----------
Adds Upwork API support to Flask.

flask-upwork version 1.0
(C) 2015 Upwork
"""

import os
from setuptools import setup

readme = open(os.path.join(os.path.dirname(__file__), 'README'))
README = readme.read()
readme.close()

version = __import__('flaskext').get_version()

setup(
    name='Flask-Upwork',
    version='1.0-pre2',
    download_url='http://github.com/strogonoff/flask-upwork',
    url='https://github.com/strogonoff/flask-upwork',
    license='BSD',
    author='Artem Gnilov',
    author_email='boobsd@gmail.com',
    maintainer='Volodymyr Hotsyk, Anton Strogonoff',
    maintainer_email='gotsyk@gmail.com, astrogov@upwork.com',
    description='Upwork API support to Flask',
    long_description=README,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'oauth2',
        'python-upwork>=1.0'
    ],
    test_suite='tests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
