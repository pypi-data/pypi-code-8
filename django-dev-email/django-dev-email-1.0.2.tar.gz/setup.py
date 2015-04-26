from setuptools import setup, find_packages

version = '1.0.2'

setup(name='django-dev-email',
      version=version,
      description="Send all mail to a desired address during development",
      long_description=open("README.md", "r").read(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 3",
          "Framework :: Django",
          "Framework :: Django :: 1.4",
          "Framework :: Django :: 1.5",
          "Framework :: Django :: 1.6",
          "Framework :: Django :: 1.7",
          "Framework :: Django :: 1.8",
          "Programming Language :: Python",
          "Topic :: Utilities",
          "License :: OSI Approved :: MIT License",
          ],
      keywords='',
      author='Derek Stegelman',
      url='http://github.com/dstegelman/django-dev-email',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
    )
