from setuptools import setup, find_packages
setup(
    name = 'django-event-logger',
    version = '0.5.0',
    packages = find_packages(),

    install_requires = ['Django'],

    author = 'Brandon B.',
    author_email = 'unaffiliate@outlook.com',
    description = 'An easy-to-use event logger for Django.',
    keywords = 'django events logger logging',
    download_url = 'https://github.com/misread/django-event-logger/tarball/0.5.0',
)
