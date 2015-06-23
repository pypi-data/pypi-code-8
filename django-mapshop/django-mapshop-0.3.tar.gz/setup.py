from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(name='django-mapshop',
      version='0.3',
      description='Internet shop with geographic points',
      long_description=readme,
      url='http://github.com/storborg/funniest',
      author='Dmitry Zharikov',
      author_email='zdimon77@gmail.com',
      license='MIT',
      packages=find_packages(exclude=["config"]),
      include_package_data=True,
      zip_safe=False) 
