from setuptools import setup

setup(
    name='simplebus-mail',
    version='0.9.5',
    packages=['simplebus_mail'],
    url='https://github.com/viniciuschiele/simplebus-mail',
    license='Apache 2.0',
    author='Vinicius Chiele',
    author_email='vinicius.chiele@gmail.com',
    description='SimpleBus-Mail is a library for Python 3 which send emails using simplebus.',
    keywords=['simplebus', 'mail', 'email', 'smtp'],
    install_requires=['simplebus==0.9.5'],
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Communications',
          'Topic :: Internet',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Networking']
)
