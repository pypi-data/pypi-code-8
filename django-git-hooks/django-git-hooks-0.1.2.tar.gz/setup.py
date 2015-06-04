# coding=utf-8
from distutils.core import setup

setup(
    name='django-git-hooks',
    version='0.1.2',
    packages=['git_hooks', ],
    requires=['django (>= 1.3)', 'gitpull'],
    url='',
    license='MIT License',
    author='Dezu',
    author_email='zhukovvitaliy@mail.ru',
    description='Небольшое приложение, для простого git pull репозитория из корня проекта при GET запросе по урлу.',
    keywords='django, git, pull',
    long_description=open('README.markdown').read(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
