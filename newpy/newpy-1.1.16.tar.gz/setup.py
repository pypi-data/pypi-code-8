from setuptools import setup

setup(
    name="newpy",
    version="1.1.16",
    py_modules=["newpy"],
    description="Quickly and easily create a new python project",
    long_description="This package aims to save time when setting up a new python project.",
    url="https://bitbucket.org/edwardonsoftware/newpy",
    download_url="https://pypi.python.org/pypi/newpy",
    author="Edward",
    author_email="edwardprentice@gmail.com",
    keywords="tutorial new example skeleton",
    license="MIT",
    packages=["resources"], #causes an indent error on install
    include_package_data=True,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
