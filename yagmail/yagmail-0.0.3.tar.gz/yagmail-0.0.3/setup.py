from setuptools import setup

setup(name='yagmail',
      version='0.0.3',
      description='Yet Another GMAIL client',
      url='https://github.com/kootenpv/yagmail',
      author='Pascal van Kooten',
      author_email='kootenpv@gmail.com',
      license='GPL',
      install_requires=[ 
          'keyring'
      ],
      zip_safe=False)
