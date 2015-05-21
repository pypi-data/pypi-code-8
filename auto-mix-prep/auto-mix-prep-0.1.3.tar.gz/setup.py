from setuptools import setup, find_packages

setup(
    name='auto-mix-prep',
    packages=find_packages(),
    install_requires=['pydub'],
    version='0.1.3',
    description='Application for automatically preparing stems for mixing.',
    entry_points={
        'console_scripts': [
            'amp=src.main:main'
        ],
    },
    author='Dashj',
    author_email='johanlovgr@gmail.com',
    url='https://github.com/dashj/auto-mix-prep',
    download_url='https://github.com/dashj/auto-mix-prep/tarball/0.1.3',
    keywords=['audio', 'music production', 'mixing'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Editors',
        'Topic :: Utilities',


    ],
)
