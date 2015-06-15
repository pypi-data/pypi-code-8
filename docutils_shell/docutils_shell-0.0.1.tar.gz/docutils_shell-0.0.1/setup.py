# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
        name='docutils_shell',
        version='0.0.1',
        description="docutils extension to insert stdout of given shell command",
        long_description=open('README.rst', 'r').read(),
        author='Paul Wexler',
        author_email="paul@prometheusresearch.com",
        license="MIT",
        url='https://bitbucket.org/pwexler/docutils_shell',
        classifiers=[
                'Programming Language :: Python',
                'Intended Audience :: Developers',
                 ],
        platforms='Any',
        keywords=('docutils', 'sphinx', 'shell', 'documentation'),
        package_dir={'': 'src'},
        packages=find_packages('src'),
        install_requires=[
                'sphinx-rtd-theme>=0.1.7, <1',
                ] 
        )

