try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='edh_python_utilities',
    version='0.0.6',
    packages=['edh_python_utilities', 'edh_python_utilities.test_scripts'],
    keywords='influence health influencehealth python utilities utility',
    url='https://github.com/medseek-engineering/edh_python_utilities/tree/0.0.1',
    license='',
    author='Eric Meisel',
    author_email='eric.meisel@influencehealth.com',
    description="Python utilities for Influence Health's Enterprise Data Hub",
    long_description=readme(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing',
        'Development Status :: 1 - Planning',
    ],
    install_requires=['python-dateutil']
)
