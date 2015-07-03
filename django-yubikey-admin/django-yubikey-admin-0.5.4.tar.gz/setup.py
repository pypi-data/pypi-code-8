#!/usr/bin/env python
import codecs
from setuptools import setup, find_packages


def read_files(*filenames):
    """
    Output the contents of one or more files to a single concatenated string.
    """
    output = []
    for filename in filenames:
        f = codecs.open(filename, encoding='utf-8')
        try:
            output.append(f.read())
        finally:
            f.close()
    return '\n\n'.join(output)


setup(
    name='django-yubikey-admin',
    version='0.5.4',
    description='Yubikey Support for the Django Admin.',
#    long_description=open('README.md').read(),
    author='Chayim Kirshen',
    author_email='chayim@lyricalsecurity.com',
    url='https://github.com/LyricalSecurity/django-yubikey-admin/',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires = [
        'yubico-client',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
    ],
)
