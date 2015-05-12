# -*- coding: utf-8 -*-

import click


OPTIONS = {
    'fullname': 'Your full name',
    'email': 'Your email',
    'pypi-login': 'Your PyPi login',
    'pypi-pass': 'Your PyPi password'
}

@click.command()
@click.option('--fullname', help=OPTIONS['fullname'])
@click.option('--email', help=OPTIONS['email'])
@click.option('--pypi-login', help=OPTIONS['pypi-login'])
@click.option('--pypi-pass', help=OPTIONS['pypi-pass'])
@click.option('--show', help='Show current configuration')
@click.pass_obj
def cli(ctx, fullname, email, pypi_login, pypi_pass, show=None):
    """ configure pymachine tool """

    if show:
        for section in ctx.config.config.sections():
            print section
    else:

        if not fullname:
            fullname = click.prompt(OPTIONS['fullname'], default=ctx.config.get('main', 'fullname'))
        if not email:
            email = click.prompt(OPTIONS['email'], default=ctx.config.get('main', 'email'))
        if not pypi_login:
            pypi_login = click.prompt(OPTIONS['pypi-login'], default=ctx.config.get('pypi', 'pypi_login'))
        if not pypi_pass:
            pypi_pass = click.prompt(OPTIONS['pypi-pass'], default=ctx.config.get('pypi', 'pypi_pass'))


        ctx.config.set('main', 'fullname', fullname)
        ctx.config.set('main', 'email', email)
        ctx.config.set('pypi', 'pypi_login', pypi_login)
        ctx.config.set('pypi', 'pypi_pass', pypi_pass)
        ctx.config.save()
