import os

import setuptools


base_dir = os.path.dirname(__file__)
module_name = 'jam'

about = {}
with open(os.path.join(base_dir, module_name, '__about__.py')) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, 'README.rst')) as f:
    long_description = f.read()


setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],

    description=about['__summary__'],
    long_description=long_description,
    license=about['__license__'],
    url=about['__uri__'],

    author=about['__author__'],
    author_email=about['__email__'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python',
    ],

    packages=[
        module_name,
    ],

    include_package_data=True,

    install_requires=[
        'Django',
        'django-floppyforms',
        'django-vanilla-views',
    ],

    #entry_points={
    #    'console_scripts': [
    #    ],
    #},
)
