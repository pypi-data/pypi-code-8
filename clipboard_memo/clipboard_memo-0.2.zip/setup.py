from setuptools import setup
import os

#Function to read README
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='clipboard_memo',
    version='0.2',
    description='A command-line clipboard manager',
    long_description=read('README.rst'),
    url='http://github.com/arafsheikh/clipboard-memo',
    author='Sheikh Araf',
    author_email='arafsheikh@rocketmail.com',
    license='MIT',
    keywords='clipboard memo manager command-line CLI',
    include_package_data=True,
    entry_points='''
        [console_scripts]
        cmemo=clipboard_memo.main:main
        cmemo_direct=clipboard_memo.direct:direct_save
    ''',
    packages=['clipboard_memo'],
    install_requires=[
        'pyperclip',
    ],
)
