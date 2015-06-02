from setuptools import setup
setup(
        name='isub',
        version="0.1.4",
        py_modules = ['isub'],
        entry_points = {
            'console_scripts':
            ['isub=isub:main'],
            },
        description="A utility CLI for TORQUE, a portable batch system",
        url="https://bitbucket.org/kmiya/isub",
        author="Kohei Miyaguchi",
        author_email="quote.curly@gmail.com",
        classifiers=[
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Utilities'
            ]
        )
