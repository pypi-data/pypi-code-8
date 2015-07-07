# Ref: http://stackoverflow.com/questions/6344076/differences-between-distribute-distutils-setuptools-and-distutils2
from setuptools import setup


setup(name='MathDict',
      version='0.1.3',
      packages=['MathDict'],
      url='https://github.com/MBALearnsToCode/PyMathDict',
      author='Vinh Luong (a.k.a. MBALearnsToCode)',
      author_email='MBALearnsToCode@UChicago.edu',
      description='Python dict / collections Mapping sub-class that can work with mathematical operators',
      long_description='(please read README.md on GitHub repo)',
      license='MIT License',
      install_requires=['FrozenDict', 'Helpy'],
      classifiers=[],   # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='math dict')
