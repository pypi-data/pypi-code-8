# Ref: http://stackoverflow.com/questions/6344076/differences-between-distribute-distutils-setuptools-and-distutils2
from setuptools import setup


setup(name='LearningRobot',
      version='0.0.0.dev',
      packages=['LearningRobot'],
      url='https://github.com/MBALearnsToCode/LearningRobot',
      author='Vinh Luong (a.k.a. MBALearnsToCode)',
      author_email='MBALearnsToCode@UChicago.edu',
      description='Robotics-related Probabilistic Reasoning & Machine Learning',
      long_description='(please read README.md on GitHub repo)',
      license='MIT License',
      install_requires=['ProbabPyReason'],
      classifiers=[],   # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='robot prob reason learning')
