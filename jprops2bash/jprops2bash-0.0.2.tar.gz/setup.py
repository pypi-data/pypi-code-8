import os
from setuptools import setup

here = os.path.dirname(__file__)
readme_rst = os.path.join(here, 'README.rst')
long_description = open(readme_rst).read()

setup(
    name='jprops2bash',
    description='Convert Java properties file to bash env var script',
    long_description=long_description,
    keywords='java properties',
    version='0.0.2',
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
