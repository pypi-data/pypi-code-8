# Licensed under a 3-clause BSD style license - see LICENSE.rst
import os


def get_package_data():
    paths = [os.path.join('data', '*.xml'),
             os.path.join('data', '*.fits'),
             os.path.join('data', '*.html'),
             ]

    return {'astroquery.ukidss.tests': paths}
