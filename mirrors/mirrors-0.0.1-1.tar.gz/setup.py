from setuptools import setup, find_packages

authors = ['Mikela Clemmons',
           'Jon Friedman',
           'Cameron Adamez']
emails = ['mclemmons@motherjones.com',
          'jfriedman@motherjones.com',
          'cadamez@motherjones.com']

setup(name='mirrors',
      version=__import__('mirrors').__version__,
      packages=find_packages(exclude=['sample_project']),
      install_requires=[
          'django-pgjson==0.2.0',
          'jsonfield==0.9.20',
          'psycopg2==2.5.4',
          'djangorestframework==2.4.4',
          'jsonschema==2.4.0',
      ],
      extras_require={
          'development': ['Sphinx>=1.2.1', 'coverage'],
      },
      # PyPI stuff, if the time ever comes
      license='MIT',
      description="Backend server for the smokejs project",
      author=", ".join(authors),
      author_email=", ".join(emails),
      long_description=open('README.rst').read(),)
