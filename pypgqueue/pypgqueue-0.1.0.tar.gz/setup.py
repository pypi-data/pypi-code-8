from setuptools import setup, find_packages

version = "0.1.0"

setup(name="pypgqueue",
      version=version,
      license="BSD",
      platforms="any",
      author="Trey Cucco",
      author_email="fcucco@gmail.com",
      packages=find_packages(),
      description="A job queue based on PostgreSQL's listen/notify features",
      url="https://github.com/treycucco/pypgqueue",
      download_url="https://github.com/treycucco/pypgqueue/tarball/master",
      install_requires=[
        "bidon",
        "psycopg2"
      ],
      package_data={"pypgqueue": ["ddl.sql"]},
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
      ])
