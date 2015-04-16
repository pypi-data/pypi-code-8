import minitest
from distutils.core import setup

setup(
    name='minitest',
    version=minitest.__version__,
    author='Colin Ji',
    author_email='jichen3000@gmail.com',
    packages=['minitest'],
    url='https://pypi.python.org/pypi/minitest',
    description='Minitest is inspired by Ruby minispec.',
    long_description=open('README.txt').read(),
)
