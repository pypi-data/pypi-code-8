from distutils.core import setup
setup(name='lazybone',
      version='0.1.1',
      py_modules=['lazybone'],
      description='Python Library for connecting to a Lazybone Bluetooth Relay',
      author='Daniel Karpinski',
      author_email='dankarpinski@hotmail.com',
      url='https://github.com/dankarpinski/lazybone',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Operating System :: POSIX :: Linux'
          ],
      install_requires=[
          "pybluez",
          "logging"
          ]
      )
