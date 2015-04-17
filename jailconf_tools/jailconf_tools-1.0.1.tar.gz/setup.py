from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='jailconf_tools',
      version='1.0.1',
      description="""A jail.conf python library to help making administration
software""",
      long_description=readme(),
      classifiers=['Development Status :: 4 - Beta',
                   'Topic :: Text Processing :: Markup',
                   'Topic :: Terminals',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: System :: Systems Administration',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4'],
      keywords='freebsd jail parser',
      url='https://github.com/bougie/jailconf_tools',
      author='David Hymonnet',
      author_email='bougie@appartland.eu',
      license='BSD',
      packages=['jailconf_tools'],
      include_package_data=True,
      zip_safe=False)
