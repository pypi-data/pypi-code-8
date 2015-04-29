import os
from distutils.core import setup

def read_README(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name = "scraptty",
    packages = ["scraptty"],
    version = "0.0.1",
    description = "A Ptt Crawler which integrates with SQL database",
    author = "Chester Tseng",
    author_email = "cwyark@gmail.com",
    url = "http://cwyark.github.io",
    license = "MIT",
    #download_url = "",
    keywords = ["ptt", "spider", "crawler", "sql"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        ],
    long_description = read_README('README.txt')
)
