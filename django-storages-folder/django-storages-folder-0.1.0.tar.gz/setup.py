from setuptools import setup


def read(filename):
    with open(filename) as f:
        return f.read()


setup(
    name='django-storages-folder',
    version='0.1.0',
    description=('django-storages-redux extension to allow separate folders '
                 'for media and static files'),
    long_description=read('README.rst'),
    author='Ryan Pineo',
    author_email='ryanpineo@gmail.com',
    license='BSD',
    url='https://github.com/RyanPineo/django-storages-folder',
    packages=['storages_folder', 'storages_folder.backends'],
    install_requires=['django-storages-redux'],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)
