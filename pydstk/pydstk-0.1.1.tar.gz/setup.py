from distutils.core import setup

CLASSIFIERS = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'Topic :: Scientific/Engineering',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
  'Programming Language :: Python :: 3.2',
  'Programming Language :: Python :: 3.3',
  'Programming Language :: Python :: 3.4',
]

setup(
  name='pydstk',
  version='0.1.1',
  description='Data Science Toolkit client library for Python',
  py_modules=['pydstk'],
  author='George Leslie-Waksman',
  author_email='george@cloverhealth.com',
  url='http://github.com/CloverHealth/pydstk',
  license='MIT',
  classifiers=CLASSIFIERS,
  install_requires=[
    'requests>=2.7.0',
  ],
  keywords='dstk',
)
