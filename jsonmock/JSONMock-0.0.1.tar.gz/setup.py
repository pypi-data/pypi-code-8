__author__ = 'anass'


from setuptools import setup


setup(
    name='JSONMock',
    packages=['jsonmock'],
    version='0.0.1',
    description='Generate a REST testing server from a json file.',
    author='Anass LAHLALI',
    author_email='anass.lahlali@hotmail.com',
    url='https://github.com/lahlali/JSONMock.py',
    keywords=['json', 'REST', 'server', 'generate'],
    install_requires=[
        'JSONtoObject'
    ],
    entry_points={
        'console_scripts': [
            'JSONMock = jsonmock.main:main',
        ]
    }
)