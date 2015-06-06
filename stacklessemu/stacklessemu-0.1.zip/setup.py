from setuptools import setup

setup(name='stacklessemu',
      version='0.1',
      description='A quick lightweight psuedo-installation of a subset of Stackless Python functionality.',
      classifiers=[
        'License :: OSI Approved :: BSD License',
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
      ],
      author='Richard Tew',
      author_email='richard.m.tew@gmail.com',
      url='https://bitbucket.org/rmtew/greenstackless',
      install_requires=['greenlet'],
      py_modules=['stackless'])
