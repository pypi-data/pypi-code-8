from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pybarm',
      version='0.0.0.0',
      description='code for controlling miscellaneous Raspberry Pi accessories',
      url='http://github.com/danmaclean/pybarm',
      author='Dan MacLean',
      author_email='maclean.daniel@gmail.com',
      license='MIT',
      packages=['pybarm'],
      install_requires=[
          'numpy',
          'matplotlib'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/ndvi_capture', 'bin/use_camera'],
      )