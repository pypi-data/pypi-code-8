from setuptools import setup

setup(
    name="Auto_Python_2014",
    version='14.1.4',
    description='The test of Mobile API',
    #long_description=read("README.rst"),
    long_description='Really, the AutoPython around.3.0',
    classifiers=[
                 'Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Text Processing :: Linguistic',
                 ],
    author='zhangziteng',
    author_email='kaku21@163.com',
    license="BSD",
    url='http://',
    #packages=find_packages(exclude=["tests.*", "tests"]),
    packages=['common','component','init','lib','reporter','testCase','util','tools'],
    install_requires=['simplejson==3.6.5'],
    #dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0'],
    zip_safe=False
)