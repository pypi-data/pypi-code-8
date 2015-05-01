from setuptools import setup, find_packages

setup(
    name             = 'ilmwetter',
    version          = '0.2',
    packages         = find_packages(),
    entry_points     = {'scrapy': ['settings = ilmwetter.settings']},
    description      = "Scrapy spider for the weather in Ilmenau",
    author           = "Wieland Hoffmann",
    install_requires = ["scrapy"],
    url              = "https://github.com/mineo/ilmwetter",
    download_url     = ["https://github.com/mineo/ilmwetter/tarball/master"],
    license          = "MIT",
    classifiers      = ["Development Status :: 4 - Beta",
                        "Environment :: Console",
                        "Framework :: Twisted",
                        "License :: OSI Approved :: MIT License",
                        "Natural Language :: English",
                        "Operating System :: OS Independent",
                        "Programming Language :: Python :: 2.7"],
)
