# Ref: http://stackoverflow.com/questions/6344076/differences-between-distribute-distutils-setuptools-and-distutils2
from setuptools import setup


setup(name='MathFunc',
      version='0.1.5',
      packages=['MathFunc'],
      url='http://github.com/MBALearnsToCode/PyMathFunc',
      author='Vinh Luong (a.k.a. MBALearnsToCode)',
      author_email='MBALearnsToCode@UChicago.edu',
      description='Python Function with Conditions and Scope',
      long_description='(please read README.md on GitHub repo)',
      license='MIT License',
      install_requires=['CompyledFunc', 'FrozenDict', 'HelpyFuncs', 'MathDict', 'SymPy'],
      classifiers=[],   # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='math func function conditions scope')
