import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'requests',
]

wsgi_requires = ['max', 'WebTest']

setup(name='maxclient',
      version='5.1',
      description='Client library wrapper to access MAX API.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
      ],
      author='UPCnet Plone Team',
      author_email='plone.team@upcnet.es',
      url='https://github.com/upcnet/maxclient',
      keywords='web pyramid pylons client',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="maxclient",
      extras_require={
          'wsgi': requires + wsgi_requires
      },
      entry_points="""
      """,
      )
