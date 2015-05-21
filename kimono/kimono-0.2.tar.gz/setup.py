from setuptools import setup

setup(name='kimono',
    version='0.2',
    description='The Kimono API Python Wrapper',
    install_requires=[
        'requests',
    ],
    url='https://github.com/vu3jej/kimono',
    author='Jithesh E J',
    author_email='mail@jithesh.net',
    license='MIT',
    packages=['kimono'],
    zip_safe=False)
