import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()
with open(os.path.join(here, 'VERSION.txt')) as f:
    VERSION = f.read().strip()


requires = [
#    'pyramid_chameleon',
#    'pyramid_handlers',
    'bisque_api',
    'bisque_base',
    ]
extras_require = {
    'lxml' : [ 'lxml' ] ,
}

data_files  = [
    ('./etc/bisque' , [ 'development.ini' ]),
]

setup(name='bisque_engine',
      version=VERSION,
      description='The BisQue module engine: build add-on modules for BisQue',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Center for BioImage Informatics',
      author_email='bisque-bioimage@googlegroups.com',
      home_page = 'http://bioimage.ucsb.edu/bisque',
      url = 'http://biodev.ece.ucsb.edu/project/bisque',
      keywords= "database image processing scientific",
      setup_requires=["hgtools"],
      packages=find_packages(),
      include_package_data=True,
      data_files = data_files,
      zip_safe=False,
      install_requires=requires,
      extras_require=extras_require,
      tests_require=requires,
      test_suite="bisque_engine",
      entry_points={
        "bisque.services" : [
            "engine_service=bq.module_engine.controllers.engine_service",
            ],
        'bisque.commands' : [
            "module = bq.module_engine.commands.module_admin:module_admin",
            "create-module = bq.module_engine.commands.create_module:create_bisque_module"
            ],
        'pyramid.scaffold':[
            'python_module = bq.module_engine.setup.scaffolds:PythonModuleTemplate',
            'matlab_module = bq.module_engine.setup.scaffolds:MatlabModuleTemplate',
            ]
        },
      )
