from distutils.core import setup

setup(
    name = "bangarang",
    packages = ["bangarang"],
    version = "0.1.2",
    description = "Offical client library for the bangarang monitoring platform",
    author = "Eliot Hedeman",
    author_email = "eliot.d.hedeman@gmail.com",
    install_requires = [
        "requests"
    ],
    url = "https://github.com/eliothedeman/python-bangarang",
    download_url = "https://github.com/eliothedeman/python-bangarang/tarball/0.1.2",
    keywords = ["bangarang", "monitoring", "analytics"],
    classifiers = [],
)
