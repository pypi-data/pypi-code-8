try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '0.4'

SETUP_DICT = dict(
    name='torch_model_client',
    packages=['torch_model_client'],
    setup_requires=['numpy'],
    test_requires=['numpy'],
    version=VERSION,
    author='zach dwiel',
    author_email='zdwiel@plotwatt.com',
    url='https://bitbucket.org/plotwatt/torch_model_server',
    description='client library for torch_model_server',
    long_description=""" A client lubrary for torch_model_server which serializes numpy
    arrays to floats, sends the data across the wire over http to the
    server and unserializes the array of floats back into a numpy
    array """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

setup(**SETUP_DICT)
