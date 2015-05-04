from setuptools import setup
def readme():
    with open('README.md') as f:
                return f.read()

setup(name='easywsgi',
      version='0.4',
      long_description=readme(),
      description='Small module to make wsgi apps easy to write, do error checking an publishe this to the client side. See github for example.',
      url='https://github.com/jorants/easywsgi',
      author='Control-K',
      author_email='jorants@gmail.com',
      license='BEER',
      packages=['easywsgi'],
      zip_safe=False)
