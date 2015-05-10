from setuptools import setup, find_packages
setup(
    name = "sdam",
    version = "0.3",
    packages = find_packages(),
    scripts = ['sdam.py'],
    install_requires = ['twisted>=15.0'],
    author = "Oleksandr Kozachuk",
    author_email = "ddeus.lp@mailnull.com",
    description = "(s)tart programs (d)aemonized (a)nd (m)onitored.",
    license = "WTFPL",
    keywords = "daemon monitoring service",
)
