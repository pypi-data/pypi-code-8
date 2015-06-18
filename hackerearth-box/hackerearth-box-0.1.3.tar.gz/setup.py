from setuptools import setup


REQUIREMENTS = [
    'fabric'
]


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    ]

setup(name='hackerearth-box',
      version='0.1.3',
      description='Python Library to facilitate automated package management on distributed servers',
      url='',
      author='Dhruv Agarwal',
      author_email='dhruv@hackerearth.com',
      license='MIT',
      packages=['hackerearth_box'],
      classifiers=CLASSIFIERS,
      keywords=''
      )
