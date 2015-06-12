from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='cvutils',
      version='0.2.4',
      description='Utilites for Computer Vision and Image Processing',
      long_description=readme(),
      url='http://github.com/bikz05/bikz05/cvutils',
      download_url = 'https://github.com/bikz05/cvutils/archive/0.2.4',
      author='Bikramjot Singh Hanzra',
      author_email='bikz.05@gmail.com',
      license='MIT',
      packages=['cvutils'],
      keywords=['computer vision', 'image procesing', ],
      install_requires=['matplotlib',],
      scripts=['bin/cvutils-resize', 'bin/cvutils-crop'], 
      zip_safe=False)
