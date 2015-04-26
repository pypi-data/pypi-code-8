from distutils.core import setup

from shrebx import shrebx

setup(name='shrebx',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description=shrebx.__doc__,
      url='https://github.com/tlevine/shrebx',
      py_modules=['shrebx'],
      version='0.0.1',
      license='AGPL',
)
