from setuptools import setup, find_packages
requires = [
    'envoy',
    'psutil',
    'python3-memcached',
    'pycrypto',
    'simple-crypt'
    ]
setup(
    name = "exon-python-libs",
    version = "0.0.23",
    install_requires=requires,
    packages = find_packages(),
	# metadata for upload to PyPI
    author = "Stephan Conrad",
    author_email = "stephan@conrad.pics",
    description = "Exon Python Library",
    license = "Apache License (2.0)",
    keywords = "exon-python-libs",
    url = "http://exon.conrad.pics",
)
