from setuptools import setup


def read(filename):
    with open(filename) as f:
        return f.read()


setup(
    name='django-array-field-select',
    version='0.1.0',
    description=('A replacement for Django\'s ArrayField with a multiple '
                 'select form field.'),
    long_description=read('README.rst'),
    author='Ryan Pineo',
    author_email='ryanpineo@gmail.com',
    license='MIT',
    url='https://github.com/RyanPineo/django-array-field-select',
    packages=['array_field_select'],
    install_requires=['Django>=1.8'],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3'
    ]
)
