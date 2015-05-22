#encoding:utf-8
from setuptools import setup, find_packages
import sys, os

version = '0.4.31'

setup(name='ici2',
      version=version,
      description="english to chinese dictionary in terminal",
      long_description="""方便程序员在terminal查询生词的小工具""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python iciba dictionary terminal translate',
      author='yuzhe realhu1989',
      author_email='huyunyan@live.cn',
      url='https://github.com/Flowerowl/ici',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'termcolor',
      ],
      entry_points={
        'console_scripts':[
            'ici = ici.ici:main'
        ]
      },
)
