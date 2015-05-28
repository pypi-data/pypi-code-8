"""
Unittests for `gpsdio_density.core`.
"""


import tempfile

from click.testing import CliRunner
import rasterio as rio

import gpsdio_density.core


def test_standard_with_res_and_shape():

    with tempfile.NamedTemporaryFile('r+') as f:
        for res_shape in (['--res', '0.05'], ['--shape', '18', '36']):
            f.seek(0)
            args = [
                'tests/data/messages1.json',
                'tests/data/messages2.json',
                '-c', 'COMPRESS=DEFLATE',
                '-c', 'PREDICTOR=2',
                '-c', 'ZLEVEL=9',
                '-c', 'BIGTIFF=NO',
                '--dtype', 'Int16',
                f.name
            ]
            args += res_shape
            result = CliRunner().invoke(gpsdio_density.core.compute_density, args)
            f.seek(0)

            assert result.exit_code is 0

            with rio.open(f.name) as actual,\
                    rio.open('tests/data/test-standard-expected.tif') as expected:
                assert actual.read(indexes=1).all() == expected.read(indexes=1).all()
