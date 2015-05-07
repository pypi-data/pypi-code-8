from setuptools import setup, find_packages

import pagerank

requires = [
        'beautifulsoup4==4.3.2',
        'utensils==0.41',
        'wsgiref==0.1.2',
        ]

setup(
    name='pagerank',
    author='Eytan Daniyalzade',
    author_email='eytan85@gmail.com',
    url='http://daniyalzade.com',
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
    install_requires=requires,
    include_package_data=True,
)

