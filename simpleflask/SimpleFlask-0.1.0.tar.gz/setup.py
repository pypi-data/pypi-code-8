from setuptools import setup
from setuptools import find_packages

setup(
    name='SimpleFlask',
    version='0.1.0',
    author='Guido Barbaglia',
    author_email='guido.barbaglia@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    description='Simple Flask application.',
    install_requires=[
        'watchdog', 'flask', 'flask-cors', 'SimpleFlaskBlueprint'
    ],
    url='http://pypi.python.org/pypi/SimpleFlask/'
)
