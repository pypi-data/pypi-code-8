try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='zflix', version='0.31',
    description='Script that seek and play torrent',
    long_description=('A CLI script that search '
                      + ' and play torrents with peerflix'),
    classifiers=[
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Video',
    ],
    author='PERALE Thomas',
    author_email='thomas.perale@openmailbox.org',
    url='https://github.com/thomacer/zflix',
    license='GPL V3',
    install_requires=[],
    packages=['src', 'src/trackers/', 'src/subtitle'],
)
