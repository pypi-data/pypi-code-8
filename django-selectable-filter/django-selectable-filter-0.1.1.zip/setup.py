from setuptools import setup, find_packages

setup(
    name='django-selectable-filter',
    version='0.1.1',
    description='The filterspec to the Django administration that allow you to filter records using the resources of django-selectable library',
    author='Gustavo Santana de Oliveira',
    author_email='gustavo.sdo@gmail.com',
    url='https://github.com/Gustavosdo/django-selectable-filter',
    keywords=[
        'django admin',
        'django filter selectable',
    ],
    install_requires=[
        "Django",
        "django-selectable",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django :: 1.7',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Environment :: Web Environment',
        'Operating System :: OS Independent'
    ],
    license='MIT',
)
