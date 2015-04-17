from distutils.core import setup, Command

class UnitTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call(['python', '-m', 'unittest', 'discover', 'tests'])
        raise SystemExit(errno)

setup(
    name='pystacks',
    version='0.1',
    packages=['pystacks', 'pystacks.layers'],
    url='https://github.com/vzhong/pystacks',
    license='MIT',
    author='Victor Zhong',
    author_email='victor@victorzhong.com',
    description='Python library for hierarchical machine learning',
    cmdclass={'test': UnitTest},
    download_url='https://github.com/vzhong/pystacks/tarball/0.1',
    keywords=['neural networks', 'machine learning'], # arbitrary keywords
)
