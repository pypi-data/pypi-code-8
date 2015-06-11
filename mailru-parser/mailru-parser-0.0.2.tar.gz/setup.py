from setuptools import setup


VERSION = "0.0.2"

setup(
    name='mailru-parser',
    description="Parse html content of Mail.ru",
    version=VERSION,
    url='https://github.com/KokocGroup/mailru-parser',
    download_url='https://github.com/KokocGroup/mailru-parser/tarball/v{}'.format(VERSION),
    packages=['mailru_parser'],
    install_requires=[
#         'pyquery==1.2.9',
#         'lxml==2.3.4',
    ],
)
