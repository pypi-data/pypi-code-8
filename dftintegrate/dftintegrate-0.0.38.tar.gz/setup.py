#!/usr/bin/env python3


from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, "
          "could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(name='dftintegrate',
      version='0.0.38',
      description='Integrate DFT data',
      long_description=read_md('README.md'),
      author='Matthew M Burbidge',
      author_email='mmburbidge@gmail.com',
      url='https://github.com/mmb90/dftintegrate',
      license='MIT',
      install_requires=[
          "argparse",
          "termcolor",
          "numpy",
          "matplotlib",
          "scipy",
      ],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS',
          'Programming Language :: Python :: 3.4',
          'Topic :: Scientific/Engineering :: Information Analysis'],
      entry_points={
          'console_scripts': [
              'dftintegrate = dftintegrate.main:main']},
      packages=['dftintegrate', 'dftintegrate.fourier'],
      scripts=['dftintegrate/main.py'],
      package_data={'tests': ['test_input/Si2x2x2/*', 'test_input/Si_medium/*',
                              'test_input/cubic/*', 'test_input/bcc/*',
                              'test_input/fcc/*', 'test_input/cbf/*',
                              'expected_output/Si2x2x2/*',
                              'expected_output/Si_medium/*']},
      include_package_data=True)
