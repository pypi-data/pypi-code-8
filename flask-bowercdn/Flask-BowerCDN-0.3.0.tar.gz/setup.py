"""
Flask-BowerCDN

Flask-BowerCDN is a Flask extension for making it easier to work with bower in
development and CDN content in production.
"""
from setuptools import setup


setup(
    name='Flask-BowerCDN',
    version='0.3.0',
    url='https://bitbucket.org/romabysen/flask-bowercdn',
    license='BSD',
    author='Lars Hansson',
    author_email='romabysen@gmail.com',
    description='Work easily with Bower and CDN content.',
    long_description=__doc__,
    py_modules=['flask_bowercdn'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask-Bower'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
