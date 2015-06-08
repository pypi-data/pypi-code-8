from setuptools import setup

setup(
    name="pytest-trialtemp",
    version="1.0.0",
    author='Jeremy Thurgood',
    author_email='firxen@gmail.com',
    url='http://github.com/jerith/pytest-trialtemp',
    license="MIT",
    description=("py.test plugin for using the same _trial_temp working"
                 " directory as trial"),
    long_description=open("README.rst", "r").read(),
    packages=["pytest_trialtemp"],
    # The following makes a plugin available to pytest.
    entry_points={
        "pytest11": ["trialtemp = pytest_trialtemp.trialtemp"],
    },
    install_requires=["pytest", "Twisted"],
)
