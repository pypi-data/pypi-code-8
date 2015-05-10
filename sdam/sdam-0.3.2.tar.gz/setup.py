from setuptools import setup, find_packages
setup(
    name = "sdam",
    version = "0.3.2",
    packages = ['sdam'],
    entry_points = {
        'console_scripts': ['sdam = sdam:main'],
    },
    install_requires = ['twisted>=15.0'],
    author = "Oleksandr Kozachuk",
    author_email = "ddeus.lp@mailnull.com",
    description = "(s)tart programs (d)aemonized (a)nd (m)onitored.",
    license = "WTFPL",
    url = "http://launchpad.net/sdam",
    keywords = "daemon monitoring service",
)
