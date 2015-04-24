from setuptools import setup, find_packages

setup(
    name="nagios-load-per-core",
    description="Nagios plugin to check load normalized by core count",
    long_description=open('README.rst').read(),
    version="0.1",
    packages=find_packages(),
    author="Carl Flippin",
    author_email="carlf@photocarl.org",
    url="https://github.com/carlf/nagios-load-per-core",
    scripts=['check-load-by-core'],
    license="MIT",
    install_requires = ['pynagios'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: MIT License'
    ]
)
