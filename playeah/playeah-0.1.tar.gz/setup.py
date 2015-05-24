from setuptools import setup, find_packages
setup(
    name = "playeah",
    description = 'playeah',
    version = "0.1",
    author = 'Fintan McEvoy',
    author_email = 'fintan.mcevoy@gmail.com',
    url = 'https://github.com/fmcevoy/playeah',
    download_url ='https://github.com/fmcevoy/playeah/tarball/0.1',
    package_dir = {'':'lib'},
    packages = find_packages('lib'),
)
