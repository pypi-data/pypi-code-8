from setuptools import setup, find_packages

setup(
    name='ris.clickatellhttp',
    version='0.0.5',
    description='Python implementation of the HTTP API for Clickatell SMS gateway',
    url='https://github.com/rwizi/clickatellhttp',
    license='Apache',

    author='Rwizi Information Systems',
    author_email='norman@ris.co.zw',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='ris clickatell sms gateway',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
)

