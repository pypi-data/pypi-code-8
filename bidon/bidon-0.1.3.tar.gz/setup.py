import os
from pip.req import parse_requirements
from setuptools import setup


def get_requirements(filename):
  if not os.path.isabs(filename):
    filename = os.path.join(proj_root, filename)
  return [str(r.req) for r in parse_requirements(filename)]


proj_root = os.path.dirname(os.path.abspath(__file__))
version = "0.1.3"

setup(name="bidon",
      version=version,
      license="BSD",
      platforms="any",
      author="Trey Cucco",
      author_email="fcucco@gmail.com",
      packages=['bidon'],
      description="A simple, easy to use, and flexible data handling library",
      url="https://github.com/treycucco/bidon",
      download_url="https://github.com/treycucco/bidon/tarball/master",
      # install_requires=get_requirements("requirements.txt"),
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3 :: Only"
      ],
      package_data={"": ["*.txt"]})
