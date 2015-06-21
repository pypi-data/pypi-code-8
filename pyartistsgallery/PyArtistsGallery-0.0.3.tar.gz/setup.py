from distutils.core import setup

setup(
    name='PyArtistsGallery',
    version='0.0.3',
    author='Eugene Andrienko',
    author_email='h0rr0rrdrag@gmail.com',
    url='https://github.com/h0rr0rrdrag0n/PyArtistsGallery',
    description='Image gallery for artists',
    packages=[
        'pagapp',
        'pagapp.admin_panel',
        'pagapp.application_api',
        'pagapp.models',
        'pagapp.public_pages',
        'pagapp.service_pages'
    ],
    package_dir={
        'pagapp': 'pagapp',
        'pagapp.admin_panel': 'pagapp/admin_panel',
        'pagapp.public_pages': 'pagapp/public_pages',
        'pagapp.service_pages': 'pagapp/service_pages'
    },
    package_data={
        'pagapp': [
            '../config.py',
            '../README.md',
            '../LICENSE',
            '../pagapp.ini',
            '../pagapp.py',
            '../requirements.txt',
            '../migrations/*.py',
            '../migrations/*.ini',
            '../migrations/*.mako',
            '../migrations/versions/*.py',
            '../static/css/*.css',
            '../static/fonts/*.woff',
            '../static/img/*.gif',
            '../static/js/*.js',
            '../templates/*.html'
        ],
        'pagapp.admin_panel': [
            'pages/*.html',
            'pages/panel-content/*.html'
        ],
        'pagapp.public_pages': ['pages/*.html'],
        'pagapp.service_pages': ['pages/*.html']
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Operating System :: POSIX :: Linux',
        'Topic :: Artistic Software',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'
    ],
    keywords=['gallery', 'art', 'standalone'],
    long_description="""\
    There is standalone web-gallery for arts and photos.
    ----------------------------------------------------

    Based on Python 3, Flask and SQLite.
    """
)
