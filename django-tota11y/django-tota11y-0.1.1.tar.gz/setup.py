import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import tota11y

setup(
    name='django-tota11y',
    version=tota11y.__version__,
    description='Easy to install Django app for tota11y - an accessibility visualization toolkit by Khan Academy (http://khan.github.io/tota11y/).',
    author='Dmitry Kozhedubov',
    author_email='hiisi13@gmail.com',
    url='https://github.com/hiisi13/django-tota11y',
    packages=[
        'tota11y',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django>=1.4.2',
    ],
    license="MIT",
    keywords=['accessibility', 'visualization'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
