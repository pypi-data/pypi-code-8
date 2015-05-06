
SETUP_INFO = dict(
    name = 'infi.app_repo',
    version = '1.0.10',
    author = 'Arnon Yaari',
    author_email = 'arnony@infinidat.com',

    url = 'https://github.com/Infinidat/infi.app_repo',
    license = 'PSF',
    description = """A user-friendly RPM/DEP repository""",
    long_description = """A user-friendly RPM/DEB repository""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'docopt>=0.6.2',
'Flask-AutoIndex>=0.5',
'Flask>=0.10.1',
'gevent>=1.0.1',
'httpie>=0.9.2',
'infi.docopt-completion>=0.2.6',
'infi.execute>=0.1.2',
'infi.gevent-utils>=0.2.1',
'infi.logging>=0.4.4',
'infi.pyutils>=1.0.8',
'infi.rpc>=0.2.2',
'infi.traceback>=0.3.11',
'ipython>=3.0.0',
'pyftpdlib>=1.4.0',
'pygments',
'pysendfile>=2.0.1',
'requests>=2.6.0',
'schematics>=0.9.post1',
'setuptools>=14.3.1',
'waiting>=1.3.0',
'zc.buildout>=2.3.1'
],
    namespace_packages = ['infi'],

    package_dir = {'': 'src'},
    package_data = {'': [
'*.css',
'*.html',
'*.ico',
'*.js',
'*.mako',
'*.png',
'*.sh',
'gpg_batch_file',
'nginx.conf',
'vsftpd.conf'
]},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = [
'app_repo = infi.app_repo.scripts:app_repo',
'eapp_repo = infi.app_repo.scripts:eapp_repo'
],
        gui_scripts = [],
        ),
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

