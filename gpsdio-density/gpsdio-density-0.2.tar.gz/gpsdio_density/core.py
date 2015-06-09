"""
Core components for gpsdio_density
"""


from __future__ import division

import logging
import math
from multiprocessing import cpu_count
from multiprocessing import Pool

import affine
import click
import gpsdio
import numpy as np
import rasterio as rio

from . import __version__


logging.basicConfig()
log = logging.getLogger('gpsdio-density')


def _cb_key_val(ctx, param, value):

    """
    Click callback to validate and convert `--opt key=val --opt key2=val2` to
    `{'key': 'val', 'key2': 'val2'}`.

    Returns
    -------
    dict
    """

    output = {}
    for pair in value:
        if '=' not in pair:
            raise click.BadParameter("incorrect syntax for KEY=VAL argument: `%s'" % pair)
        else:
            key, val = pair.split('=')
            output[key] = val

    return output


def _cb_bbox(ctx, param, value):

    """
    Click callback to validate a bounding box.

    Returns
    -------
    tuple
        (x_min, y_min, x_max, y_max)
    """

    x_min, y_min, x_max, y_max = value
    if (x_min > y_max) or (y_min > y_max):
        raise click.BadParameter('self-intersection: {bbox}'.format(value))

    return value


def _cb_res(ctx, param, value):

    """
    Click callback to validate and transform `--res`.  Forces all values to be
    positive.  If `--res` is only given once then the value is used for both
    X and Y.

    Returns
    -------
    tuple
        Element 0 is X res and element 1 is y res.
    """

    value = tuple(map(abs, value))

    # If no values are given still return the value.  There is an error check
    # later that ensures --res OR --shape are given.
    if len(value) is 2 or len(value) is 0:
        return value
    elif len(value) is 1:
        return value[0], value[0]
    else:
        raise click.BadParameter('specified too many times.')


def _cb_shape(ctx, param, value):

    """
    Click callback to validate `--shape`.

    Returns
    -------
    tuple
        (height, width)
    """

    for v in value:
        if not v >= 1:
            raise click.BadParameter('values must be >= 1')

    return value


def _processor(args):

    """
    Create an empty numpy array, open a file, and iterate over all the messages
    with latitude and longitude.  Every time a point intersects an array element
    the element gets a +1.

    Parameters
    ----------
    args : dict
        ctx_obj : dict
            The `ctx.obj` from the parent Click context if it is a dictionary,
            or an empty dict.
        filepath : str
            Path to the file to process.
        meta : dict
            Metadata for a `rasterio` raster.  There are issues pickling
            `affine.Affine()` so `meta['transform']` are the affine elements
            as a tuple and a local instance of `affine.Affine()` is
            constructed before processing.
        field : str or None
            If summing a field rather than computing density this is the field name.

    Returns
    -------
    np.array
    """

    ctx_obj = args['ctx_obj']
    filepath = args['filepath']
    meta = args['meta']
    field = args['field']

    filter_expr = "isinstance(msg.get('lat'), (int, float)) and " \
                  "isinstance(msg.get('lon'), (int, float))"

    if field is not None:
        filter_expr += " and '%s' in msg" % field

    log.debug("Starting %s" % filepath)
    log.debug("Filter expr: %s" % filter_expr)

    data = np.zeros((meta['height'], meta['width']), dtype=meta['dtype'])
    width = meta['width']
    height = meta['height']
    aff = meta['transform']
    with gpsdio.open(filepath, driver=ctx_obj.get('i_drv'),
                     compression=ctx_obj.get('i_cmp')) as src:
        for msg in gpsdio.filter(
                src, "isinstance(msg.get('lat'), (int, float)) and "
                     "isinstance(msg.get('lon'), (int, float))"):
            col, row = (msg['lon'], msg['lat']) * ~aff
            if 0 <= row < height and 0 <= col < width:
                if field is not None:
                    val = msg[field]
                else:
                    val = 1
                data[row][col] += val

    return data


@click.command(name='density')
@click.version_option(__version__, prog_name='gpsdio-density')
@click.argument('infiles', nargs=-1, required=True)
@click.argument('outfile', required=True)
@click.option(
    '-c', '--creation-option', 'creation_options', metavar='NAME=VAL',
    callback=_cb_key_val, multiple=True,
    help='Driver-specific creation options for output raster.'
)
@click.option(
    '-f', '--format', '--driver', metavar='NAME', default='GTiff',
    help='Output format. (default: GTiff)'
)
@click.option(
    '-j', '--jobs', type=click.IntRange(1, cpu_count()), default=1,
    help='Number of files to process in parallel. (default: 1)'
)
@click.option(
    '--bbox', metavar='X_MIN Y_MIN X_MAX Y_MAX', nargs=4, type=click.FLOAT,
    default=(-180, -90, 180, 90), callback=_cb_bbox,
    help='Only process data within the specified bounding box.  '
         '(default: -180, -90, 180, 90)'
)
@click.option(
    '-n', '--nodata', type=click.FLOAT, default=None,
    help="Nodata value for output raster. (default: None)"
)
@click.option(
    '--res', metavar='RES [RES]', type=click.FLOAT, multiple=True, callback=_cb_res,
    help="Output resolution in georeferenced units.  Cannot be combined with `--shape`."
)
@click.option(
    '-s', '--shape', type=click.INT, nargs=2, metavar="ROWS COLS", callback=_cb_shape,
    help="Output shape in rows and cols.  Cannot be combined with `--res`."
)
@click.option(
    '--crs', default='EPSG:4326',
    help="Specify CRS for input points and output raster.  No transformations are performed. "
         "(default: EPSG:4326)"
)
@click.option(
    '--dtype', default=rio.int32, metavar='TYPE',
    help="Numpy datatype to use for output raster.  (default: int32)"
)
@click.option(
    '--field', metavar='NAME',
    help="Rather than computing density, sum a field.  Each point that intersects a pixel "
         "will add the value of the specified field instead of just adding 1.  Make sure "
         "to match field type with `--dtype`."
)
@click.pass_context
def compute_density(ctx, infiles, outfile, creation_options, driver, jobs, bbox,
              shape, res, crs, dtype, nodata, field):

    """
    Create a density raster from positional messages.

    Message data is streamed but the rasters are held in-memory so the max
    output resolution for the entire world is about 0.05.  Specifying a bbox
    allows for a smaller cell size but does not allow for global rasters.
    """

    log.setLevel(ctx.obj['verbosity'])

    x_min, y_min, x_max, y_max = bbox

    if res and not shape:
        x_res, y_res = res
        width = math.ceil((x_max - x_min) / x_res)
        height = math.ceil((y_max - y_min) / y_res)
    elif shape and not res:
        height, width = shape
        x_res = (x_max - x_min) / width
        y_res = (y_max - y_min) / height
    else:
        raise click.BadParameter('must specify `--res` OR `--shape`')

    meta = {
        'driver': driver,
        'height': height,
        'width': width,
        'transform': affine.Affine(x_res, 0.0, x_min, 0.0, -y_res, y_max),
        'crs': crs,
        'dtype': dtype,
        'nodata': nodata,
        'count': 1
    }
    meta.update(**creation_options)

    open_options = {
        'i_drv': ctx.obj['i_drv'],
        'i_cmp': ctx.obj['i_cmp'],
        'i_drv_opts': ctx.obj['i_drv_opts'],
        'i_cmp_opts': ctx.obj['i_cmp_opts']
    }

    task_generator = (
        {
            'ctx_obj': open_options,
            'filepath': fp,
            'meta': meta,
            'field': field
        } for fp in infiles)

    with rio.open(outfile, 'w', **meta) as dst:

        output = sum(
            (a for a in Pool(jobs).imap_unordered(_processor, task_generator)))

        dst.write(output.astype(dst.meta['dtype']), indexes=1)


if __name__ == '__main__':
    compute_density()
