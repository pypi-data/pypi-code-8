# ilp - a tag based file indexer
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is Free Software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from setuptools import setup

import subprocess

from ilp.utils import check_program


def make_manpage():
    subprocess.call([
        "a2x", "--format", "manpage", "README.txt"])


if check_program("a2x"):
    make_manpage()
else:
    print("WARNING: asciidoc is not installed, can't generate man page.")

setup(name='ilp',
      description='a tag-based file indexer',
      long_description="""
      ilp is a tool to index, tag, and search through collections of files.
      """,
      version='0.2',
      author='slowpoke',
      author_email='mail+python at slowpoke dot io',
      url='https://github.com/slowpoketail/ilp',
      install_requires=['plac'],
      packages=['ilp', 'ilp.cmdline', 'ilp.utils', 'ilp.database'],
      data_files=[
          ("/usr/share/man/man1", ("ilp.1",)),
          ("/usr/share/doc/ilp", ("README.txt",))],
      entry_points={
          'console_scripts': [
              'ilp = ilp.cmdline:main']},
      classifiers=['Environment :: Console',
                   'Development Status :: 4 - Beta',
                   'License :: Public Domain',
                   'Programming Language :: Python :: 3'],
      license='ANTI-LICENSE')
