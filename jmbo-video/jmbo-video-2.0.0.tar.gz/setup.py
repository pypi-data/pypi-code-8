from setuptools import setup, find_packages

setup(
    name='jmbo-video',
    version='2.0.0',
    description='Jmbo video application.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Consulting',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/jmbo-video',
    packages = find_packages(),
    install_requires = [
        'django-ckeditor>=4.2.1',
        'jmbo>=2.0.3',
    ],
    tests_require=[
        'django-setuptest>=0.1.4',
        'psycopg2',
    ],
    test_suite='setuptest.setuptest.SetupTestSuite',
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
