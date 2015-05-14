from setuptools import setup, find_packages

setup(
    name='nio-cli',

    version='0.1.11',

    description='Command line tools for n.io',

    url='https://github.com/neutralio/nio-cli',

    author='n.io',
    author_email='info@n.io',

    packages=['nio_cli', 'nio_cli.util', 'nio_cli.actions', 'nio_cli.nio_add_blocks'],

    install_requires = [
        'prettytable',
        'requests'
    ],

    entry_points={
        'console_scripts': [
            'nio=nio_cli.main:_nio_instance_main'
        ]
    },

    keywords=['nio']
)
