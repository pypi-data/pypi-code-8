from setuptools import setup

setup(name='cran',
      version='0.1.3',
      description='Cran via Native Python Library Wrapping',
      url='http://github.com/mindey/cran',
      author='Mindey I.',
      author_email='mindey@qq.com',
      license='MIT',
      packages=['cran'],
      install_requires=[
          'GitPython',
          'pandas',
          'numpy',
          'scipy',
          'pylab',
      ],
      zip_safe=False)
