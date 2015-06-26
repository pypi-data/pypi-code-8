from setuptools import setup, find_packages

setup(
    name='pyf.station',
    version='2.0.5',
    description=(
        "PyF.Station is a protocol with client and server implementation "
        "to transfer python generators accross tcp networks."
    ),
    long_description=open("README.txt").read(),
    # Get more strings
    # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords='python generator tcp/ip',
    author='',
    author_email='',
    url='http://pyfproject.org',
    license='MIT',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['pyf'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'twisted',
        'pyf.transport>=2.0',
        'pyjon.events',
        'simplejson'
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
