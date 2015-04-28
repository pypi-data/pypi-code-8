
from setuptools import setup

setup(
    name='twentyc.database',
    version='0.1.1',
    author='Twentieth Century',
    author_email='code@20c.com',
    description='database abstractions',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=[
      'twentyc.database',
      'twentyc.database.couchdb',
      'twentyc.database.couchbase'
    ],
    url = 'https://github.com/20c/twentyc.database',
    download_url = 'https://github.com/20c/twentyc.database/tarball/0.1.0',
    install_requires=[
      "CouchDB==0.9"
    ],
    namespace_packages=['twentyc'],
    zip_safe=False
)
