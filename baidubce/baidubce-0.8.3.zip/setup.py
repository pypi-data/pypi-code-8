from distutils.core import setup

setup(
    name='baidubce',
    version='0.8.3',
    packages=['baidubce',
              'baidubce.auth',
              'baidubce.http',
              'baidubce.services',
              'baidubce.services.bos'],
    url='http://bce.baidu.com',
    license='',
    author='baidu.com',
    author_email='',
    description='Python sdk for baidu bce'
)