from setuptools import setup

setup(
    name='auto-mix-prep',
    packages=['auto-mix-prep'],
    install_requires=['pydub'],
    version='0.1',
    description='Application for automatically preparing stems for mixing.',
    entry_points={
        'console_scripts': [
            'amp = package.module:main'
        ],
    },
    author='Dashj',
    author_email='johanlovgr@gmail.com',
    url='https://github.com/dashj/auto-gain-stage',
    download_url='https://github.com/dashj/auto-gain-stage/tarball/0.1',
    keywords=['audio', 'music production', 'gain', 'staging'],
    classifiers=[],
)
