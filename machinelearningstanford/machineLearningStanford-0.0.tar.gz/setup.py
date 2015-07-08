#!/usr/bin/env python3

from setuptools import setup

setup(
    name = 'machineLearningStanford',
    version = '0.0',
    description = 'Machine Learning Stanford',
    author = 'Lai, Chih-An',
    author_email = 'chihan.lai@gmail.com',
    url = 'https://github.com/ZianLai/machineLearningStanford',
    packages = ['ex1', 'ex2', 'ex3'],
    install_requires=[
        'numpy',
    ],
    py_modules = ['ex1.linearRegression', 'ex2.logisticRegression', 
          'ex3.multiClassification'],
    zip_safe = False 
    )
