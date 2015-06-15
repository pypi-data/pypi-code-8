from setuptools import find_packages, setup

from rts import __version__


EXCLUDE_FROM_PACKAGES = []

setup(
    name='django-rts',
    version=__version__,
    url='http://www.djangoproject.com/',
    author='Jos van Velzen',
    author_email='jos.vanvelzen@changer.nl',
    description=('A django app that provides building blocks to receive requests, transform data and send '
                 'the response .'),
    license='BSD',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
