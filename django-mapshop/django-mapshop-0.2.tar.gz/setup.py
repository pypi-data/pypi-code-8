from setuptools import setup, find_packages

setup(name='django-mapshop',
      version='0.2',
      description='Internet shop with geographic points',
      url='http://github.com/storborg/funniest',
      author='Dmitry Zharikov',
      author_email='zdimon77@gmail.com',
      license='MIT',
      packages=find_packages(exclude=["config"]),
      include_package_data=True,
      zip_safe=False) 
