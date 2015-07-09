from setuptools import setup


setup(name='CompyledFunc',
      version='0.1.8',
      packages=['CompyledFunc'],
      url='https://github.com/MBALearnsToCode/CompyledFunc',
      author='Vinh Luong (a.k.a. MBALearnsToCode)',
      author_email='MBALearnsToCode@UChicago.edu',
      description='Compiled functions via Sympy/Theano',
      long_description='(please read README.md on GitHub)',
      license='MIT License',
      install_requires=['HelpyFuncs', 'NumPy', 'SymPy', 'Theano'],
      classifiers=[],   # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='sympy theano compile')
