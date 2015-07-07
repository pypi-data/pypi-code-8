# -*- coding: utf-8 -*-

"""
MarcoPolo utilities
"""

from setuptools import setup, find_packages
import os, glob, sys, stat

if __name__ == "__main__":

    here = os.path.abspath(os.path.dirname(__file__))
    
    with open(os.path.join(here, 'DESCRIPTION.rst')) as f:
        long_description = f.read()


    data_files = [
                     ('/usr/local/bin', glob.glob("usr/local/bin/*"))
                 ]

    if "install" in sys.argv:
        for f in glob.glob("usr/local/bin/*"):
            os.chmod(f, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    setup(
        name="marcopolo-shell",
        namespace_packages=['marcopolo'],
        provides=['marcopolo.utils'],
        version="0.0.3",
        description="A set of useful utilities for MarcoPolo",

        long_description=long_description,

        url='marcopolo.martinarroyo.net',

        author='Diego Martín',

        author_email='martinarroyo@usal.es',

        license='MIT',
        include_package_data=True,
        classifiers=[
            'Development Status :: 3 - Alpha',

            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            
            'Operating System :: POSIX :: Linux',

            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',

            'Topic :: System :: Networking',
            'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',

            'Natural Language :: English',
        ],

        keywords="marcopolo shell utilities",
        
        install_requires=["marcopolo>=0.0.1", "marcopolo.bindings>=0.0.1"],
        
        zip_safe=False,
        
        data_files=data_files,
        packages=find_packages(),
        entry_points={
            'console_scripts': ['marcodiscover = marcopolo.utils.marcodiscover:main',
                                'marcoinstallkey = marcopolo.utils.marcoinstallkey:main'
                                ],
        },

    )

    
