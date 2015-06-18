from distutils.core import setup

setup(
    name='phjs-manager',
    version='0.0.9',
    author="michey",
    author_email='mixeyy@gmail.com',
    packages=["app"],
    include_package_data=True,
    url="http://pypi.python.org/pypi/MyApplication_v010/",
    description="Useful towel-related stuff.",
    install_requires=['docker-py', 'flask'],
)