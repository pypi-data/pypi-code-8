from setuptools import setup, find_packages
setup(
    name = "sdam",
    version = "0.3.1",
    packages = find_packages(),
    entry_points = {
        'console_scripts': ['sdam = sdam:main'],
    },
    install_requires = ['twisted>=15.0'],
    author = "Oleksandr Kozachuk",
    author_email = "ddeus.lp@mailnull.com",
    description = "(s)tart programs (d)aemonized (a)nd (m)onitored.",
    license = "WTFPL",
    keywords = "daemon monitoring service",
)
