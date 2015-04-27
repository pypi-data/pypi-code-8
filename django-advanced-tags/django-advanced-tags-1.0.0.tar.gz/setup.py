from distutils.core import setup
import os


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name='django-advanced-tags',
    version='1.0.0',
    packages=['advanced_tags', 'advanced_tags.templatetags', ],
    url='https://bitbucket.org/buffagon/django-advanced-tags',
    license='GNU LGPL',
    author='Alex Prokofiev',
    author_email='prokofiev.ad@yandex.ru',
    description=read("README"),
    requires=['django', ]
)
