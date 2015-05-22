from setuptools import setup, find_packages

setup(
    name='cern-sso',
    version='0.1.1',
    url='https://github.com/scr4t/cernsso',
    author='Alexander Baranov',
    author_email='sashab1@yandex-team.ru',
    packages=find_packages(),
    description='Python wrapper around cern-get-sso-cookie',
    install_requires=[
        "sh==1.11",
    ],
    tests_require=[
        "nose==1.3.4",
        "nose-testconfig==0.9",
    ],
)
