from setuptools import setup
import exlogging


def parse_requirements():
    with open('requirements.txt') as f:
        return [l.strip() for l in f.readlines() if not l.startswith('#')]


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='exlogging',
    version=exlogging.__version__,
    description="Supports to setup python standard logging package.",
    long_descriptiondescription=readme(),
    classifiers=[
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    license=exlogging.__license__,
    author=exlogging.__author__,
    author_email='motoki@naru.se',
    url='https://github.com/narusemotoki/exlogging',
    keywords=' '.join(['log', 'logging', 'logger']),
    zip_safe=False,
    install_requires=parse_requirements(),
)
