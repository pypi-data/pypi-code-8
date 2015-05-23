import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pystache',
    ]

docs_extras = [
    'Sphinx',
    'docutils',
    'repoze.sphinx.autointerface',
    ]

testing_extras = [
    'nose',
    'coverage',
    'virtualenv', # for scaffolding tests
    ]

setup(name='pyramid_pystache',
      version='0.1',
      description='Mustache template bindings using Pystache for the Pyramid web framework',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Intended Audience :: Developers",
        "License :: Repoze Public License",
        "Topic :: Text Processing :: Markup :: HTML",
        ],
      author="Darren Lucas",
      author_email="me@darrenlucas.com",
      url="https://github.com/darrenlucas/pyramid_pystache",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      extras_require = {
          'testing':testing_extras,
          'docs':docs_extras,
          },
      test_suite="pyramid_pystache",
      entry_points="""\
      """,
      )
