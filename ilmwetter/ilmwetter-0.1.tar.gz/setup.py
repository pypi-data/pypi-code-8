from setuptools import setup, find_packages

setup(
    name         = 'ilmwetter',
    version      = '0.1',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = ilmwetter.settings']},
    description  = "Scrapy spider for the weather in Ilmenau",
    author       = "Wieland Hoffmann",
    install_requires = ["scrapy"]
)
