from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='sascar_client',
      version='1.2',
      description="A client to sascar soap web service.",
      long_description=long_description,
      keywords='',
      author="Wille Marcel",
      author_email='wille@wille.blog.br',
      url='https://github.com/ibamacsr/sascar_client',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'suds',
          'psycopg2',
          'shapely',
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      sascar_client=sascar_client.scripts.cli:cli
      """,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Programming Language :: Python :: 2 :: Only',
          ]
      )
