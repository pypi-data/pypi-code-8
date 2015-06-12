from setuptools import setup, find_packages

import pypbs

setup(
    name = pypbs.__projectname__,
    version = pypbs.__release__,
    packages = find_packages(),
    author = pypbs.__authors__,
    author_email = pypbs.__authoremails__,
    description = pypbs.__description__,
    license = "GPLv2",
    keywords = pypbs.__keywords__,
    entry_points = {
        'console_scripts': [
            'pbsstatus = pypbs.pbsstatus:main',
            'qpeek = pypbs.qpeek:main',
        ],
    },
)
