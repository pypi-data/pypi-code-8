import os
from setuptools import setup


def read(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='govuk-template',
    version='0.1.6',
    description='The GOV.UK template for python',
    url='https://github.com/LandRegistry/python-govuk-template',
    license='MIT',
    author='Ramin Vazir <ramin.vazir@digital.landregistry.gov.uk>,\
            Michael Allen <michael@michaelallen.io>',
    packages=[
        'govuk_template.flask.assets',
        'govuk_template.flask.mustache'
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
    ],
    install_requires=['flask', 'pystache'],
)
