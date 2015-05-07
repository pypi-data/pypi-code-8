from setuptools import setup, find_packages

import pagerank

requires = [
        'beautifulsoup4',
        'utensils',
        'wsgiref',
        ]

setup(
    name='pagerank',
    author='Eytan Daniyalzade',
    author_email='eytan85@gmail.com',
    url='http://daniyalzade.com',
    install_requires=requires,
    packages=find_packages(),
    description='Utility to get pagerank of keywords on google',
    long_description=open('README.rst').read(),
    version=pagerank.__version__,
    data_files=[
        ('', ['README.rst']),
        ],
    package_dir={
        'pagerank': 'pagerank'
        },
    include_package_data=True,
)

