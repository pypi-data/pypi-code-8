from setuptools import setup, find_packages


setup(name='coinop',
      version='0.2.0',
      description='Crypto-currency conveniences',
      url='http://github.com/GemHQ/coinop-py',
      author='Matt Smith',
      author_email='matt@gem.co',
      license='MIT',
      packages=find_packages(exclude=[
          u'*.tests', u'*.tests.*', u'tests.*', u'tests']),
      install_requires=[
          'PyNaCl==0.3.0',
          'cffi',
          'pytest',
          'pycrypto',
          'python-bitcoinlib==0.4.0',
          'pycoin==0.52',
          'PyYAML',
          'ecdsa'
      ],
      zip_safe=False)
