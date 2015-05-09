from distutils.core import setup

with open('README.rst') as f:
    LONG_DESCRIPTION=f.read()
    f.close()

setup(
    name='django-project-goblin',
    version='1.3',
    description='Manage list of projects',
    long_description=LONG_DESCRIPTION,
    author="Jordan Hewitt",
    author_email='jordannh@sent.com',
    license='GPLv3',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License' +
            ' v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords = 'project software version development management django',
    url='https://gitorious.org/django-project-goblin',

    packages=['goblin',],
)
