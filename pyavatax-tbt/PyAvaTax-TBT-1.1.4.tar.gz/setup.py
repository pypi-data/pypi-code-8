from distutils.core import setup
# python setup.py sdist
# python setup.py sdist bdist_wininst upload

version = __import__('pyavatax').get_version()

setup(
    name='PyAvaTax-TBT',
    url = 'http://github.com/lionheart/pyavatax/',
    author = 'Dan Loewenherz',
    author_email = 'dan@lionheartsw.com',
    version=version,
    install_requires = ['requests==1.1', 'decorator==3.4.0', 'suds==0.4'],
    package_data = {
        '': ['*.txt', '*.rst', '*.md']
    },
    packages=['pyavatax',],
    license='BSD',
    long_description="PyAvaTax is a Python library for easily integrating Avalara's RESTful AvaTax API Service",
)
