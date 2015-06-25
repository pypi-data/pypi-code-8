import os

from setuptools import setup


def get_packages(package):
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}

setup(
    name='django-love-utils',
    version='0.1.1',
    url='https://github.com/ailove-dev/django-love-utils',
    license='MIT',
    author='Ailove',
    author_email='ailove@ailove.com',
    description='Utils for django project',
    packages=get_packages('love_utils'),
    package_data=get_package_data('love_utils'),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'django>=1.7',
    ],
    tests_require=['Django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)