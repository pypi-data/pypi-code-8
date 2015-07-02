from setuptools import setup, find_packages


setup(
    name='plotta',
    version='1.0.1a1',
    install_requires=['unirest'],

    author='Guido Zuidhof',
    author_email='me@guido.io',
	
	packages=find_packages(),

    description='Python wrapper for Plotta API',
    url='https://github.com/gzuidhof/plotta-python',
    license='MIT',
    keywords='plot plotting plotta',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ]
)
