try:
    from setuptools.command.install import install as _install
    from setuptools import setup
except ImportError:
    from distutils.command.install import install as _install
    from distutils.core import setup


MESSAGE = ('Please install ppy before continuing. '
           'Run `pip install ppy` and try again.')


class install(_install):
    def run(self):
        raise EnvironmentError(MESSAGE)


setup(
    name='useppy',
    version='0.1.3',
    description='Stops the install process with instructions to install ppy.',
    long_description='',
    author='Joe Esposito',
    author_email='joe@joeyespo.com',
    url='http://github.com/joeyespo/useppy',
    license='MIT',
    platforms='any',
    packages=[],
    install_requires=['ppy'],
    cmdclass={'install': install},
)
