#!/usr/bin/python
from setuptools import setup, find_packages


from staggered_selects import __version__, __version_info__


github_url = 'https://github.com/datahub/django-staggered-selects'
github_tag_version = __version__


setup(
    name='django-staggered-selects',
    version=__version__,
    description='Staggered drop-down menus for the Django admin',
    url=github_url,
    download_url='%s/tarball/%s' % (github_url, __version__),
    author='Allan James Vestal',
    author_email='datahub@jrn.com',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
