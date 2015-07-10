from distutils.core import setup

setup(
    name='SIDEKIT',
    version='0.1.10',
    author='Anthony Larcher',
    author_email='anthony.larcher@univ-lemans.fr',
    packages=['sidekit'],
    url='http://pypi.python.org/pypi/Sidekit/',
    license='COPYING.LESSER',
    description='Speaker Recognition and Diarization package.',
    long_description=open('README.txt').read(),
    install_requires=[
        "mock==1.0.1",
        "nose==1.3.4",
        "numpy>=1.9.0",
        "pyparsing==2.0.2",
        "python-dateutil==2.2",
        "scipy>=0.14.0",
        "six==1.8.0",
        "wsgiref==0.1.2",
        "matplotlib == 1.3.1",
    ],
)




