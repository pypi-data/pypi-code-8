from setuptools import setup, find_packages
import sys
import os

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload -r pypi")
    sys.exit()

setup(
    name='guardiancl',
    version='0.0.9',
    description='Computer system information for GuardianCL',
    long_description='guardiancl is a system information for GuardianCL using data mainly served by psutil',
    classifiers=[
        'Topic :: System :: Monitoring',
        'Topic :: System :: Logging',
        'Topic :: System :: Networking :: Monitoring',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='monitoring web iot',
    author='WeboneSystem',
    author_email='suporte@webonesystem.com.br',
    url='https://github.com/guardiaocl/guardiaocl-servers.git',
    license='Apache',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'APScheduler==3.0.3',
        'psutil==3.0.1',
        'configparser2==4.0.0'
    ],
    entry_points={
        'console_scripts': [
            'guardiancl = guardiancl.run:main'
        ]
    }
)