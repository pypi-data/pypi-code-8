from setuptools import setup


setup(
    description="Easy peasy wrapper for HipChat's v1 API (modified version and credits to kurttheviking)",
    name='python-hipchat-v1',
    url='https://github.com/greenietea/python-hipchat-v1',
    version='0.3.3',
    packages=['hipchat'],
    author='Greenie',
    author_email='hello@greenie.ninja',
    license='MIT',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
