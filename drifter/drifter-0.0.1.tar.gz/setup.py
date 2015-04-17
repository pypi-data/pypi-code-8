from setuptools import setup

with open('README.rst') as h_rst:
    LONG_DESCRIPTION = h_rst.read()

with open('docs/changes.rst') as h_rst:
    BUF = h_rst.read()
    BUF = BUF.replace('``', '$')        # protect existing code markers
    for xref in [':meth:', ':attr:', ':class:', ':func:']:
        BUF = BUF.replace(xref, '')     # remove xrefs
    BUF = BUF.replace('`', '``')        # replace refs with code markers
    BUF = BUF.replace('$', '``')        # restore existing code markers
LONG_DESCRIPTION += BUF

DESCRIPTION = "VirtualBox control and documentation mechanism"


setup(
    name='drifter',
    version='0.0.1',
    py_modules=['drifter', 'virtualbox'],
    include_package_data=True,
    install_requires=[
        'click',
        'pyyaml',
        'colorama',
    ],
    entry_points='''
        [console_scripts]
        drifter=drifter:cli
    ''',
    # metadata for upload to PyPI
    author="Jeff Hinrichs",
    author_email="jeffh@dundeemt.com",
    description=DESCRIPTION,
    license="BSD",
    keywords="VirtualBox Vagrant Development",
    url="https://bitbucket.org/dundeemt/drifter",   # project home page
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    download_url='https://pypi.python.org/pypi/drifter',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

)
