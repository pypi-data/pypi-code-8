from setuptools import setup


setup(
    name='jprops2bash',
    description='Convert Java properties file to bash env var script',
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',
    keywords='java properties',
    version='0.0.1',
    author='Marc Abramowitz',
    author_email='msabramo@gmail.com',
    install_requires=['setuptools', 'jprops'],
    url='https://github.com/msabramo/jprops2bash',
    license='MIT',
    py_modules=['jprops2bash'],
    entry_points={
        'console_scripts': [
            'jprops2bash = jprops2bash:main',
        ],
    },
    zip_safe=False,
)
