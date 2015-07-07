from setuptools import setup, find_packages

setup(
    name='ProxmoxDriver',
    version='0.1.0',
    description='Driver for communicating with a proxmox API.',
    author='Thomas Steinert',
    author_email='monk@10forge.org',
    url='https://github.com/m-o-n-k/ProxmoxDriver',
    license='MIT',
    packages=find_packages(
        exclude=[
            'bin',
            'docs',
            'test',
            'venv'
        ]
    ),
    install_requires=[
        'requests==2.6.2',
    ],
    tests_require=[
        'bottle==0.12.8',
        'pytest==2.7.0',
    ]
)
