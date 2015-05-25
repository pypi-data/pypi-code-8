from setuptools import setup

setup(
    name='tprofile',
    version='0.0.13',
    packages=['tprofile'],
    author='timchow',
    author_email='jingjiang@staff.sina.com.cn',
    license='LGPL',
    install_requires=["tornado>=3.1.1"],
    description="a profile tool for tornado web requesthandler",
    keywords='tornado profile',
    url='http://tieba.baidu.com/f?ie=utf-8&kw=%E5%91%A8%E4%BA%95%E6%B1%9F',
    entry_points={
        "console_scripts":[
            "test_tprofile_server=tprofile.test_server:main",
        ],
    },
    package_data={
        'tprofile': ['usage.txt'],
    },
    long_description=open("tprofile/usage.txt").read()
)

