from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='pd-sprintstats',
      version='3.2.2',
      description='Gathers some statistics for a sprint from JIRA',
      author='Jason Diller',
      author_email='jdiller@pagerduty.com',
      url='',
      install_requires=required,
      scripts=['sprintstats', 'wikifysprint'],
      packages=['lib', 'templates'],
      pacakge_data={'templates':'templates/*.j2'},
      include_package_data=True,
)
