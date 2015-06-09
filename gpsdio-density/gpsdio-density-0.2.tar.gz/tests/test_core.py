"""
Unittests for `gpsdio_density.core`.
"""


import tempfile

from click.testing import CliRunner
import gpsdio.cli
import rasterio as rio

import gpsdio_density


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
                '-c', 'INTERLEAVE=BAND',
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


def test_with_field():

    with tempfile.NamedTemporaryFile('r+') as f:
        result = CliRunner().invoke(gpsdio.cli.main.main_group, [
            'density',
            'tests/data/messages1.json',
            'tests/data/messages2.json',
            '--res', '10',
            '--field', 'val',
            '--dtype', 'Int16',
            '-c', 'COMPRESS=DEFLATE',
            '-c', 'PREDICTOR=2',
            '-c', 'ZLEVEL=9',
            '-c', 'BIGTIFF=NO',
            '-c', 'TILED=YES',
            '-c', 'INTERLEAVE=BAND',
            f.name
        ])
        f.seek(0)
        print(result.output)
        assert result.exit_code is 0

        with rio.open(f.name) as actual, \
                rio.open('tests/data/test-with-field-expected.tif') as expected:

            assert actual.meta == expected.meta
            assert actual.read(indexes=1).all() * 2 == expected.read(indexes=1).all()
            assert expected.bounds == actual.bounds == (-180, -90, 180, 90)


def test_version():
    result = CliRunner().invoke(gpsdio.cli.main.main_group, [
        'density',
        '--version'
    ])

    assert result.exit_code is 0

    assert 'gpsdio-density' in result.output and gpsdio_density.__version__ in result.output
