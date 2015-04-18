import click
from geobricks_raster_correlation.core.raster_correlation_core import get_correlation

@click.command()
@click.argument('file1', nargs=1)
@click.argument('file2', nargs=1)
@click.option('--bins', default=150, help='The number of bins applied.')
def cli_get_correlation(file1, file2, bins):
    try:
        corr = get_correlation(file1, file2, bins)
        click.echo('Series: %s' % corr['series'])
        click.echo('Stats: %s' % corr['stats'])
    except Exception, e:
        click.echo(e)


if __name__ == '__main__':
    cli_get_correlation()