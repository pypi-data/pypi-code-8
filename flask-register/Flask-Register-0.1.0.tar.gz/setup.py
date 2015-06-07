"""
Flask-Register
--------------

Flask-Register provides that can turn on/off Register view function.

Links
`````
* Github : https://github.com/cryptosan/flask-register
"""
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

ext_path = os.path.join(os.path.dirname(__file__), 'flask_register.py')
ver_line = [line for line in open(ext_path) if line.startswith('__version__')]
__ver__ = ver_line[0].split('=')[1].strip().replace('\'', '')


setup(
    name='Flask-Register',
    version=__ver__,
    url='https://github.com/cryptosan/flask-register/',
    license='MIT',
    author='Cryptos An',
    author_email='frostlabx@gmail.com',
    description='Register ext for Flask',
    long_description=__doc__,
    py_modules=['flask_register'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
