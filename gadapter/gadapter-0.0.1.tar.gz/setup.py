from setuptools import setup
from setuptools import find_packages


def readme():
    return open("README.md", "r").read()


REQUIREMENTS = ["gcloud", "six"]

setup(
    name='gadapter',
    packages=find_packages(),
    version='0.0.1',
    long_description=readme(),
    description='Adapter for Gcloud - python',
    author='plasmashadow',
    author_email='plasmashadowx@gmail.com',
    url='https://github.com/RevelutionWind/gadapter.git',
    license='Apache 2.0',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Environment :: Console'
    ],
    install_requires=REQUIREMENTS,
    test_suite="test"
)