from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pygenenet',
      version='0.1.1',
      description='Python implementation of GeneNet algorithm (Barker et al. 2011)',
      url='',
      author='Trang Tran',
      author_email='ttdtrang@gmail.com',
      license='MIT',
      packages=['pygenenet'],
      install_requires=[ 'numpy>=1.8.0',
                         'pandas>=0.15.2',
                         'graphviz>=0.4.3'
                        ],
      extras_require = { 'timing':  ["matplotlib"] },
      zip_safe=False)
