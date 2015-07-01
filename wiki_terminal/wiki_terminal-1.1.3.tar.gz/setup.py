__author__ = 'cm'
from setuptools import setup, find_packages, Extension

setup(name='wiki_terminal',
      version='1.1.3',
      description="This script will enable you use wikipedia in terminal. This is inspired by longcw's youdao.",
      long_description="""
            Install:
                        you can install it by python setup.py\n

            Help:\n
                        wiki -h(--help)for help\n

                        wiki -s(--summary) argto get summary about the arg\n

                        wiki -S(--search) argto search arg on wiki\n

                        wiki -r(--random) s(summary)to get a random tittle (you can get summary about it if you want.)\n

                        wiki -g(--geosearch) latitude longitude (radius) Do a wikipedia geo search for latitude and longitude using.\n

                        wiki -H(--history) show your search history and allow you to search again easily.\n

                        wiki -c(--clrhis) clear your query history.\n

            Version:\n
                        Version 1.0.0 basic function built\n
                        Version 1.0.1 the geosearch function is added\n
                        version 1.1.0 the keyword-highlight function is added\n
                        version 1.1.1 the search function bug fixed and history function added\n
                        version 1.1.2 some problem fixed
                        version 1.1.3 some problem fixed
                        """,
      keywords='python wikipedia terminal',
      author='cm',
      author_email='jason0916phoenix@gmail.com',
      url='https://github.com/JASON0916/wiki_terminal',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'termcolor', 'wikipedia',
          ],
      classifiers=[
          'Programming Language :: Python :: 2.7',
      ],
      entry_points={
          'console_scripts': [
              'wiki = wiki.main:main',
          ]
      },
)