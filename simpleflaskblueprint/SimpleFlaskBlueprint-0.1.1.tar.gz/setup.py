from setuptools import setup
from setuptools import find_packages

setup(
    name='SimpleFlaskBlueprint',
    version='0.1.1',
    author='Guido Barbaglia',
    author_email='guido.barbaglia@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    description='Simple Flask blueprint.',
    install_requires=[
        'watchdog', 'flask', 'flask-cors'
    ],
    url='http://pypi.python.org/pypi/SimpleFlaskBlueprint/'
)
