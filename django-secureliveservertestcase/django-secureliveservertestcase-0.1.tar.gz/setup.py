from setuptools import setup

setup(name="django-secureliveservertestcase",
      version="0.1",
      description="Adds a SSL server for testing in Django",
      url="http://github.com/pbrooks/django-secureliveservertestcase",
      author="Peter Brooks",
      author_email="spamme@pbrooks.net",
      license="MIT",
      packages=['secureliveservertestcase'],
      install_requires=['Django >= 1.8', 'pyOpenSSL']
      )
