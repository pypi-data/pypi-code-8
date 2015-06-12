from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='cvutils',
      version='0.2',
      description='Utilites for Computer Vision and Image Processing',
      long_description=readme(),
      url='http://github.com/bikz05/bikz05/cvutils',
      download_url = 'https://github.com/bikz05/cvutils/archive/master.zip',
      author='Bikramjot Singh Hanzra',
      author_email='bikz.05@gmail.com',
      license='MIT',
      packages=['cvutils'],
      keywords=['computer vision', 'image procesing', ],
      install_requires=['matplotlib',],
      scripts=['bin/cvutils-resize'],
      zip_safe=False)
