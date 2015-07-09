from distutils.core import setup
import os.path

README = os.path.join(os.path.dirname(__file__), 'README.md')

version = '1.0'

with open(README) as fp:
    longdesc = fp.read()

setup(name='ignore-from-github',
    include_package_data=True,
    version=version,
    description='Add common sets of ignored file types to your .gitignore easily',
    long_description=longdesc,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development',
        'Intended Audience :: Developers'
    ],
    author='Anson Rosenthal',
    author_email='anson.rosenthal@gmail.com',
    license='MIT License',
    url='https://github.com/anrosent/ignore.git',
    scripts=['ignore']
)
