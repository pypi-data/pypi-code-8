import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djmailgun',
    version='0.0.1',
    description='A simple drop-in mail backend for Django',
    long_description=README,

    install_requires=['requests>=2.5.1'],

    include_package_data=True,
    packages=find_packages(),

    license='MIT License',
    url='http://www.example.com/',
    author='Dmitry Yuzhakov',
    author_email='dmtry88@gmail.com',
    keywords="django mailgun email",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)