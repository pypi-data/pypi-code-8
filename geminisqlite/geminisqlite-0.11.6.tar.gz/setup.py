import os
from setuptools import setup

version_py = os.path.join(os.path.dirname(__file__), 'geminisqlite', 'version.py')
version = open(version_py).read().strip().split('=')[-1].replace('"', '')
long_description = """
``geminisqlite` is a database framework for exploring genetic variation'
"""

with open("requirements.txt", "r") as f:
    install_requires = [x.strip() for x in f.readlines() if not x.startswith("geminisqlite")]

setup(
        name="geminisqlite",
        version=version,
        install_requires=install_requires,
        requires=['python (>=2.5, <3.0)'],
        packages=['geminisqlite',
                  'geminisqlite.scripts',
                  'geminisqlite.data'],
        author="Aaron Quinlan and Uma Paila.",
        description='A database framework for exploring genetic variation',
        long_description=long_description,
        url="http://geminisqlite.readthedocs.org",
        package_dir={'geminisqlite': "geminisqlite"},
        package_data={'geminisqlite': [
            'static/css/geminisqlite.css',
            'static/img/geminisqlite.png',
            'static/third_party/bootstrap/css/*',
            'static/third_party/bootstrap/img/*',
            'static/third_party/bootstrap/js/*',
            'static/third_party/jquery/jquery-1.7.1.js',
            'static/third_party/jquery-ui/jquery-ui.min.js',
            'views/*'
            ]},
        zip_safe=False,
        include_package_data=True,
        scripts=['geminisqlite/scripts/geminisqlite'],
        author_email="brecht.gossele@student.kuleuven.be",
        classifiers=[
            'Development Status :: 3 - Alfa',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Topic :: Scientific/Engineering :: Bio-Informatics']
    )
