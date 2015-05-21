from setuptools import setup

setup(name='kimono',
    version='0.2.2',
    description='Python wrapper for kimonolabs API',
    long_description=open('README.rst').read(),
    install_requires=[
        'requests',
    ],
    url='https://github.com/vu3jej/kimono',
    author='Jithesh E J',
    author_email='mail@jithesh.net',
    license='MIT',
    packages=['kimono'],
    zip_safe=False)
