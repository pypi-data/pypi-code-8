from setuptools import setup, find_packages

setup(
    name='python-watch-cantrips',
    version='0.0.1',
    namespace_packages=['cantrips'],
    packages=find_packages(),
    url='https://github.com/luismasuelli/python-watch-cantrips',
    license='LGPL',
    author='Luis y Anita',
    author_email='luismasuelli@hotmail.com',
    description='Python watch cantrips. This will behave as AngularJS\'s cantrips',
    install_requires=['python-cantrips>=0.6.6']
)