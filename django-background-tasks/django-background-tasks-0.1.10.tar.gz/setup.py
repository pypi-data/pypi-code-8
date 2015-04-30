from setuptools import setup, find_packages

version = __import__('background_task').__version__

setup(
    name='django-background-tasks',
    version=version,
    description='Database backed asynchronous task queue',
    long_description=open('README.rst').read(),
    author='arteria GmbH, John Montgomery',
    author_email='admin@arteria.ch',
    url='http://github.com/arteria/django-background-tasks',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
