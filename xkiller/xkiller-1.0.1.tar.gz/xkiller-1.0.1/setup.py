from distutils.core import setup

setup(
    name = "xkiller",
    packages = [],
    version = "1.0.1",
    description = "Daemon that kills X sessions",
    author = "Kaashif Hymabaccus",
    author_email = "kaashif@kaashif.co.uk",
    url = "http://github.com/kaashif/py-xkiller",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers"
    ],
    scripts = ["xkiller"],
    requires = ["daemonize"]
)
