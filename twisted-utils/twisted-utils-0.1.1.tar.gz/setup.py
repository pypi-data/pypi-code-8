from distutils.core import setup
import twutils
setup(name='twisted-utils',
      packages=['twutils'],
      description='Simple utils for twisted extracted for reuse',
      author='Franz Eichhorn',
      author_email='frairon@googlemail.com',
      url='https://bitbucket.org/eh14/twisted-utils',
      license='MIT',
      version=twutils.__version__,
      )
