from setuptools import setup, find_packages

setup(
    name="zc.time",
    description="Hook time for testing",
    long_description=open("src/zc/time/README.txt").read(),
    version="1.0.2",
    license="ZPL 2.1",
    packages=find_packages('src'),
    include_package_data=True,
    package_data={"zc.time": ["*.txt"]},
    zip_safe=False,
    package_dir={'': 'src'},
    namespace_packages=['zc'],
    install_requires=[
        'pytz',
        'setuptools',
        ],
    )
