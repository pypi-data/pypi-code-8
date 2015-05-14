from setuptools import setup, find_packages

setup(
    name="offyt",
    version="0.1.3",
    packages=[],
    scripts=['offyt.py'],

    install_requires=[
        'docopt==0.6.2',
        'filelock==1.0.3',
        'youtube-dl==2015.5.10',
    ],

    author="Koen Bollen",
    author_email="meneer@koenbollen.nl",
    description="Offline YouTube Playlist Synchronization",
    license="ISC",
    keywords="youtube offline playlist synchronization download",
    url="https://github.com/koenbollen/offyt"
)
