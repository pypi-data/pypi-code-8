from distutils.core import setup

setup(
    name='summics',
    version='1.1.0',
    author=u'Brand a Trend GmbH',
    packages=['summics'],
    data_files=[('./', ['readme.md'])],
    license='BSD-2-Clause, see LICENCE.txt',
    description='Summics API',
    zip_safe=True,
)
