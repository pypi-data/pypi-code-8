from setuptools import setup

setup(
    name='redact',
    url='https://github.com/zweifisch/redact',
    version='0.1.1',
    description='rendering config files from templates',
    author='Feng Zhou',
    author_email='zf.pascal@gmail.com',
    packages=['redact'],
    install_requires=['opster', 'cliui'],
    entry_points={
        'console_scripts': ['redact=redact:redact'],
    },
)
