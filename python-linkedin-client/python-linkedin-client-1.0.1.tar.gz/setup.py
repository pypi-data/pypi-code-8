#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

setup(
    author='Ming Chen',
    author_email='mockey.chen@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ],
    description='LinkedIn API in python',
    keywords=['linkedin', 'rest api', 'oauth2', 'linkedin profile'],
    license='MIT',
    long_description=readme,
    name='python-linkedin-client',
    packages=['python_linkedin_client'],
    url='https://github.com/mingchen/python-linkedin-client',
    download_url ='https://github.com/mingchen/python-linkedin-client/releases',
    version='1.0.1',
    install_requires=['Python >= 2.6'],
)

