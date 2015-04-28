
from setuptools import setup

setup(
    name='twentyc.tools',
    version='0.1.4',
    author='Twentieth Century',
    author_email='code@20c.com',
    description='various python tool libraries / helpers',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url='https://github.com/20c/twentyc.tools',
    download_url='https://github.com/20c/twentyc.tools/tarball/0.1.2',
    packages=['twentyc.tools'],
    install_requires=[
      "Markdown==2.5.2",
      "prettytable==0.7.2",
      "python-daemon==1.6",
      "unittest2==0.8.0"
    ],
    namespace_packages=['twentyc'],
    zip_safe=False
)
