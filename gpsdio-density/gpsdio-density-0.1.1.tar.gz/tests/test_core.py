"""
Unittests for `gpsdio_density.core`.
"""


import tempfile

from click.testing import CliRunner
import gpsdio.cli
import rasterio as rio


def test_standard_with_res_and_shape():

    with tempfile.NamedTemporaryFile('r+') as f:
        for res_shape in (['--res', '10'], ['--shape', '18', '36']):
            f.seek(0)
            args = [
                '--i-drv', 'NewlineJSON',
                'density',
                'tests/data/messages1.json',
                'tests/data/messages2.json',
                '-c', 'COMPRESS=DEFLATE',
                '-c', 'PREDICTOR=2',
                '-c', 'ZLEVEL=9',
                '-c', 'BIGTIFF=NO',
                '-c', 'TILED=YES',
                '--dtype', 'Int16',
                f.name
            ]
            args += res_shape
            result = CliRunner().invoke(gpsdio.cli.main.main_group, args)
            f.seek(0)

            assert result.exit_code is 0

            with rio.open(f.name) as actual,\
                    rio.open('tests/data/test-standard-expected.tif') as expected:

                assert actual.meta == expected.meta
                assert actual.read(indexes=1).all() == expected.read(indexes=1).all()

                # If the affine or transform is not properly written then
                # one of these will be incorrect.  Should have world extent.
                assert expected.bounds == actual.bounds == (-180, -90, 180, 90)
