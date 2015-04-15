from setuptools import setup
setup(
    name='Gavagai',
    packages=['gavagai'],
    version='0.1',
    description='A Gavagai API helper library.',
    author = 'Johan Dewe',
    author_email = 'johan@dewe.net',
    url = 'https://github.com/dewe/gavagai-python',
    keywords = ['text-analysis', 'api', 'nlp'], 
    license='The MIT License (MIT)',
    install_requires=[
        'requests>=2.6.0,<3.0',
        'urllib3',
        'ndg-httpsclient',
    ]
)