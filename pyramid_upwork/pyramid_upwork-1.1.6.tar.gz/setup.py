import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'pyramid>=1.5a2',
    'python-upwork>=1.0.0',
    'pyramid_redis_sessions>=1.0a1'
]

setup(name='pyramid_upwork',
      version='1.1.6',
      description='pyramid_upwork',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
      ],
      author='Cyril Panshine',
      author_email='kipanshi@gmail.com',
      url='https://github.com/kipanshi/pyramid_upwork',
      keywords='web pyramid pylons authentication upwork oauth',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="pyramid_upwork",
      )
