# Test for Python version 2 only
import sys
if not sys.version_info[0] == 2:
    print "Sorry, but Python 3 isn't inherently supported yet"
    sys.exit(1)

from setuptools import setup, find_packages

setup(name='pyfck',
      version='0.1',
      description=u"A bare-bones Brainfuck interpreter written in Python 2.7. It's guaranteed to have bugs",
      classifiers=[],
      keywords='brainfuck interpreter command-line',
      author=u"Wes Gilleland",
      author_email='wes.gilleland@gmail.com',
      url='https://github.com/Deathnerd/pyfck',
      download_url='https://github.com/Deathnerd/pyfck@master',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      package_data={
          'pyfck': [
              'LICENSE',
              'README.md',
              'pyfck/__init__.py',
              'pyfck/getch.py',
              'pyfck/scripts/__init__.py',
              'pyfck/scripts/cli.py',
              'tests/conway.bf',
              'tests/main.bf',
              'tests/rot13.bf',
              'test_cli.py',
              'test_mod.py'
          ]
      },
      zip_safe=False,
      install_requires=[
          'click'
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      pyfck=pyfck.scripts.cli:cli
      """
      )
