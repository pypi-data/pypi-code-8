from setuptools import setup


setup(
    name='django-wfs',
    packages=['django-wfs'],
    version='0.0.2',
    description='A WFS (web feature service) implementation as a Django application.',
    author='Vasco Pinho',
    author_email='vascogpinho@gmail.com',
    url='https://github.com/vascop/django-wfs',
    download_url='https://github.com/vascop/django-wfs/tarball/master',
    long_description=open('README.md', 'r').read(),
    license='Apache 2.0',
    keywords=['wfs', 'geo', 'django'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
    ],
)
