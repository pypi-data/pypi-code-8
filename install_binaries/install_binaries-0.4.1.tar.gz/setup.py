from setuptools import setup


setup(
    name = "install_binaries",
    version = "0.4.1",
    author = "Thomas Grenfell Smith",
    author_email = "smithtg@ncbi.nlm.nih.gov",
    description = "Install binaries to the same place Python would install scripts.",
    long_description = open('README.md').read(),
    url = "https://github.com/tgs/install-binaries",

    py_modules = ['install_binaries'],

    entry_points = {
        'distutils.commands': [
            'install_binaries = install_binaries:install_binaries',
        ],
        'distutils.setup_keywords': [
            'install_binaries = install_binaries:handle_install_binaries',
        ],
    },

    classifiers = [
        'License :: Public Domain',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
    ],
)
