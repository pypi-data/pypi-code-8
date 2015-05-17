from setuptools import setup

setup(name='iabjad',
      version='0.2',
      description='Utilities to work with Abjad from IPython',
      url='https://github.com/cryptonomicon314/iabjad.git',
      author='Cryptonomicon',
      author_email='cryptonomicon.314@gmail.com',
      license='MIT',
      packages=['iabjad'],
      install_requires=[
          'abjad'
      ],
      zip_safe=False)
