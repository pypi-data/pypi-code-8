from setuptools import setup

setup(
    name='db_url',
    version='0.3.3',
    license='Public Domain',
    description='connect to the DATABASE_URL environment variable',
    url='https://github.com/razzius/db_url/',
    long_description=open('README.md').read(),
    py_modules=['db_url'],
    entry_points={
        'console_scripts': [
            'db=db_url:connect_to_database'
        ]
    }
)
