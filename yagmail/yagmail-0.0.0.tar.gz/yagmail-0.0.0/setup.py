from setuptools import setup

setup(name='yagmail',
      version='0.0.0',
      description='Yet Another GMAIL client',
      url='https://www.linkedin.com/profile/view?id=190745232',
      author='Pascal van Kooten',
      author_email='kootenpv@gmail.com',
      license='GPL',
      install_requires=[ 
          'keyring',
          'email',
          'smptlib'
      ],
      zip_safe=False)
