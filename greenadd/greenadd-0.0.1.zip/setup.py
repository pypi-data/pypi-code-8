from setuptools import setup, find_packages

setup(
    name = 'greenadd',
    version = '0.0.1',
    keywords = ('greenadd', 'egg'),
    description = 'a simple egg',
    license = 'MIT License',

    url = 'http://www.baidu.com',
    author = 'greenadd',
    author_email = 'i@green.org',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)