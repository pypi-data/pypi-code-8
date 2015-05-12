# -*- coding: utf-8 -*-

import click

DEV_STATUS = {
    'Planning': "Development Status :: 1 - Planning",
    'Pre-Alpha': "Development Status :: 2 - Pre-Alpha",
    'Alpha': "Development Status :: 3 - Alpha",
    'Beta': "Development Status :: 4 - Beta",
    'Production/Stable': "Development Status :: 5 - Production/Stable",
    'Mature': "Development Status :: 6 - Mature",
    'Inactive': "Development Status :: 7 - Inactive",
}

DEV_STATUS_KEYS = [key.lower() for key in DEV_STATUS.keys()]


@click.command()
@click.argument('name')
@click.option('--description', help='Description of the machine pack')
@click.option('--version', help='Version of machinepack', default='0.1')
@click.option('--author', help="Author's full name")
@click.option('--email', help="Author's email")
@click.option('--dev_status', type=click.Choice(DEV_STATUS_KEYS), default='planning')
@click.pass_obj
def cli(ctx, name, description, author, email, dev_status, version):
    """ create new machinepack """

    # basic checks
    ctx.machinepack_viewer.check_machine_path(name)

    if not author:
        author = ctx.config.get('main', 'fullname') or click.prompt('Your fullname')
        ctx.config.set('main', 'fullname', author).save()

    if not email:
        email = ctx.config.get('main', 'email') or click.prompt('Your email')
        ctx.config.set('main', 'email', author).save()

    if not description:
        description = click.prompt('Description of the machinepack')

    dev_status = DEV_STATUS[dev_status.title()]

    classifiers = [
        dev_status,
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]

    params = {
        'machinepack_name': name,
        'machinepack_description': description,
        'author': author,
        'author_email': email,
        'classifiers': classifiers,
        'version': version,
        'keywords': " ".join(['machinepack']),
    }
    ctx.machinepack_viewer.create_basic_structure(params)

    ctx.echo('')
    ctx.echo.success('Create successful!')
    ctx.echo("To start run:\n    cd %s\n    pymachine" % ('machinepack_' + name))

