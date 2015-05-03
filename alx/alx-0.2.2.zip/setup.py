from distutils.core import setup

setup(
    name='alx',
    version='0.2.2',
    url='https://github.com/gomes-/alx',
    license='GPLv3+',
    author='Alex Gomes',
    author_email='gomes@alexgomes.com',
    description='Swiss army knife for Shell, Cloud and DevOps.',

    scripts=['bin/alx.py',
             'bin/alx.bat',
             'bin/alx',
             ],
    packages=['alx', 'alx.data'],


    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Networking ',
        'Topic :: System :: Shells',
        'Topic :: System :: Systems Administration',
        ],
)
