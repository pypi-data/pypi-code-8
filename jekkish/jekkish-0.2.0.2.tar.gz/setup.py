from setuptools import setup

setup(
    name='jekkish',
    version='0.2.0.2',

    description='A CLI frontend for pdftex for easy templated LaTeX writing.',
    long_description=open('README.rst').read(),

    url='https://github.com/joshjzaslow/latex-jekkish',
    download_url='https://github.com/joshjzaslow/latex-jekkish/tarball/0.2',

    author='Josh Zaslow',
    author_email='josh.zaslow@gmail.com',
    maintainer='Josh Zaslow',
    maintainer_email='josh.zaslow@gmail.com',

    license='MIT',
    packages=['jekkish'],
    include_package_data=True,

    keywords=['LaTeX'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Markup :: LaTeX',
    ],
    requires=['PyYAML', 'Jinja2'],
    install_requires=['PyYAML', 'Jinja2'],
    entry_points={
        "console_scripts": ['jekkish=jekkish.jekkish:main']
    },
)
