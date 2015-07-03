from setuptools import setup

setup(name='vpopulus_api',
      version='0.2.2',
      description='An API for the vPopulus browser game',
      url='https://github.com/ca1ek/vpopulus_api',
      author='ca1ek',
      author_email='ca1ekowy@gmail.com',
      license='MIT',
      packages=['vpopulus_api'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)