from setuptools import setup, Extension, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

parse = Extension('relay.parse', sources=['relay/parse.c'])

setup(name="relay-framework",

      version="0.2.0",

      description="Relay is an irc micro-framework "
                  "that smells too much like a web framework",

      long_description=long_description,

      url="https://github.com/ldesgoui/relay",

      classifiers=[
              "Development Status :: 3 - Alpha",
              "Topic :: Communications :: Chat :: Internet Relay Chat",
              "License :: OSI Approved :: MIT License",
              "Programming Language :: Python :: 2.7",
              "Programming Language :: Python :: 3.4",
      ],

      keywords="irc internet relay chat framework",

      author="Lucas Desgouilles",
      author_email="ldesgoui@gmail.com",

      license="MIT",
      # see LICENSE for more informations

      packages=find_packages(exclude=["tests*"]),

      ext_modules=[parse],
)
