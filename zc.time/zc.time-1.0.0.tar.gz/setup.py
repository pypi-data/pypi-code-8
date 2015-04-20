from setuptools import setup, find_packages

setup(
    name="zc.time",
    description="Hook time for testing",
    long_description=open("src/zc/time/README.txt").read(),
    version="1.0.0",
    license="ZPL 2.1",
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},
    namespace_packages=['zc'],
    install_requires=[
        'pytz',
        'setuptools',
        ],
    )
