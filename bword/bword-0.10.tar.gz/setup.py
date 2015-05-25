from setuptools import setup, find_packages

setup(
      name='bword',
      version='0.10',
      description="a console translation dictionary used dict.baidu.com Api",
      keywords='python english translation dictionary terminal',
      author='zhanghang',
      author_email='stevezhang@gmail.com',
      url='https://github.com/zhanghang-z',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'requests',
      ],
      entry_points={
        'console_scripts':[
            'bword = bword.bword:main'
        ]
      },
)
