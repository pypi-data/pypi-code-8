from setuptools import setup

setup(name='efacter',
      version='0.1.2',
      description = ("facter client with extended functionality "
                     "and Facter class to work with complex facts"),
      url='http://github.com/CSXbot/efacter',
      author='Mikhail Tuzikov',
      author_email='tuzikov@gmail.com',
      license='Creative Commons Attribution 4.0 International License',
      packages=['efacter'],
      keywords='facter puppet',
      install_requires=['pygments'],
      entry_points={
          'console_scripts': [
              'efacter=efacter:main',
          ],
      },
      )
