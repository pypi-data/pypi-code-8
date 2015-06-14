try:
    from setuptools.command.install import install as _install
    from setuptools import setup
except ImportError:
    from distutils.command.install import install as _install
    from distutils.core import setup


MESSAGE = 'Requirement ppy now installed. Please run again.'


class install(_install):
    def run(self):
        import sys
        print(sys.argv)
        raise EnvironmentError(MESSAGE)


setup(
    name='useppy',
    version='0.1.5',
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
