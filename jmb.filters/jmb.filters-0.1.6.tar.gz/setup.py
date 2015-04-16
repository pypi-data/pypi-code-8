import os
from setuptools import setup, find_packages

f = open('README.rst')
readme = f.read()
f.close()

def get_data_files(*args, **kwargs):

    EXT_PATTERN = kwargs.get('ext') or '\.(html|js|txt|css|po|mo|png|json|xml|yml)'

    data_dict = {}
    for pkg_name in args:
        data_files = []
        for dirpath, dirnames, filenames in os.walk(pkg_name.replace('.', '/')):
            rel_dirpath = re.sub("^" + pkg_name + '/', '',  dirpath)
            # Ignore dirnames that start with '.'
            for i, dirname in enumerate(dirnames):
                if dirname.startswith('.'): del dirnames[i]
            if filenames:
                data_files += [os.path.join(rel_dirpath, f) for f in filenames
                               if re.search(EXT_PATTERN, f)]
        data_dict[pkg_name] = data_files
    return data_dict

setup(
    name='jmb.filters',
    namespace_packages = ['jmb'],
    version='0.1.6',
    description=('jmb.filters is a reusable Django application for allowing'
                 ' users to filter querysets dynamically.'),
    long_description=readme,
    author='Alex Gaynor, Alessandro Dentella',
    author_email='sandro@e-den.it',
    url='http://github.com/alex/django-filter/tree/master',
    packages=find_packages(exclude=['tests', 'test_project', 'test_project.*',]),
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    package_data=get_data_files('jmb.filter')
    # package_data={
    #     'jmb.filters' : [
    #           'jmb.filters/locale/it/LC_MESSAGES/django.mo',
    #           'jmb.filters/tests/templates/tests/book_filter.html'
    #           ],
    #  }
    
)
