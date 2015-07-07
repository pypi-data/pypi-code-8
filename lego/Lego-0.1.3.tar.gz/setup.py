# ref: http://stackoverflow.com/questions/6344076/differences-between-distribute-distutils-setuptools-and-distutils2
# ref: https://packaging.python.org/en/latest/distributing.html
# ref: http://peterdowns.com/posts/first-time-with-pypi.html

from setuptools import setup


setup(name='Lego',
      version='0.1.3',
      packages=['Lego'],
      url='https://github.com/MBALearnsToCode/Lego',
      author='Vinh Luong (a.k.a. MBALearnsToCode)',
      author_email='MBALearnsToCode@UChicago.edu',
      description='Lego',
      long_description='Miscellaneous Python "helper" functions',
      license='MIT License',
      install_requires=[],
      classifiers=[],   # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='lego')
