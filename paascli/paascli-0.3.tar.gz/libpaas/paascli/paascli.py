__author__ = 'hvishwanath'


import click
import os
import sys
import base64
import json
from db import *
from libpaas import settings
from libpaas.drivers.manager import DriverManager
from config import Config
from libpaas.camp import pdpparser

@click.group(help="Manage your applications across PaaS providers")
def paascli():
    Config.getInstance()
    db_init()


@paascli.group(help="Manage paas providers")
def provider():
    pass


@paascli.command(help="Reset configuration and local cache")
def reset():
    c = raw_input("This will delete local cache and configuration. All local data will be lost. Proceed [N/y]? : ")
    if c:
        c= c.upper()
        if c == "Y":
            Config.getInstance().reset()
            db_reset()
            click.echo("Removed all configuration and local cache information")
            return

    click.echo("Command aborted.")


@paascli.command(help="Refresh local cache from cloud")
def refresh():
    c = raw_input("This will delete local app cache. It will be refreshed from providers in the cloud. Proceed [N/y]? : ")
    if c is None:
        click.echo("Command aborted.")
        return

    c = c.upper()
    if c != "Y":
        click.echo("Command aborted.")
        return

    if Provider.select().count() <= 0:
        click.echo("There are no configured providers. Try <paascli providers add>")

    try:
        click.echo("Removing local cache..")
        if Application.select().count() > 0:
            for app in Application.select():
                app.delete_instance(recursive=True)


        click.echo("Refreshing app cache from configured Providers\n----------------------------------------")
        for p in Provider.select():
            click.echo("Contacting %s....." % p.providername)
            d = DriverManager.getInstance()
            driver = d.find_driver(p.providername)

            if driver is None:
                click.echo("No driver available for %s" % p.providername)
                continue

            click.echo("Driver for %s is %s" % (provider, str(driver)))
            di = driver(p.username, p.password)
            r = di.list_apps()
            if r is None:
                click.echo("Error retrieving app details from %s" % p.providername)
                continue

            # Make a database Entry
            for a in r:
                a = Application(appid=a["appid"], giturl=a["giturl"], weburl=a["weburl"], provider=p)
                a.save()
                click.echo("Added entry. %s" % str(a))

        click.echo("Refresh complete")
    except Exception as ex:
        click.echo("Error during refresh: %s. If you find cache/config data inconsistent, try <paascli reset>" % str(ex))


@provider.command(help="Add a paas provider")
@click.option('--name', required=True, prompt=True)
@click.option('--user', required=True, prompt=True)
@click.password_option()
def add(name, user, password):
    p = base64.b64encode(password)
    p = Provider(providername=name, username=user, password=p)
    try:
        p.save()
        click.echo('Added provider %s successfully' % name)

    except Exception as ex:
        click.echo("Error adding provider : %s" % str(ex), color="red")



@provider.command(help="List configured paas providers")
def list():
    if Provider.select().count() > 0:
        click.echo("Configured Providers\n-----------------------")
        for p in Provider.select():
            click.echo("%s - Username: %s" %(p.providername, p.username))
    else:
        click.echo("No providers are configured yet.", color="red")


@provider.command(help="Delete a configured provider")
@click.option('--name', required=True, prompt=True)
def delete(name):
    try:
        p = Provider.get(Provider.providername == name)
        p.delete_instance()
        click.echo("Deleted provider %s" % name)
    except DoesNotExist:
        click.echo("No provider entry with name : %s" % name)
    except Exception as ex:
        click.echo("Error completing command : %s" % str(ex))


@paascli.group(help="Manage applications")
def app():
    pass


@app.command(help="Install an app on a configured paas platform")
@click.option('--provider', required=True, prompt=True)
@click.option('--appid', required=True, prompt=True)
@click.option('--pdparchive', required=True, prompt=True)
def install(provider, appid, pdparchive):

    try:
        pdr = Provider.get(Provider.providername == provider)
    except Exception as ex:
        click.echo("Error getting provider info for %s" % provider)
        pdr = None

    if pdr is None:
        return

    try:
        p = pdpparser.PDPParser(pdparchive)
        click.echo("Parsed Plan: \n%s" % str(p.plan))
        d = DriverManager.getInstance()
        driver = d.find_driver(provider)
        if driver is None:
            click.echo("No driver available for %s" % provider)
            return

        click.echo("Driver for %s is %s" % (provider, str(driver)))
        di = driver(pdr.username, pdr.password)
        r = di.install_app(appid, p)
        if r is None:
            click.echo("Error during app installation")
            return

        # Make a database Entry
        appid, giturl, weburl = r
        a = Application(appid=appid, giturl=giturl, weburl=weburl, provider=pdr)
        a.save()

    except Exception as ex:
        click.echo("Error: %s" % str(ex))


@app.command(help="Uninstall an app from a configured paas platform")
@click.option('--appid', required=True, prompt=True)
def uninstall(appid):

    try:
        app = Application.get(Application.appid== appid)
    except Exception as ex:
        click.echo("Error getting application info for %s" %  appid)
        click.echo("Try refreshing your config database <paascli refresh>")
        app = None
        return

    try:
        d = DriverManager.getInstance()
        provider = app.provider.providername
        driver = d.find_driver(provider)
        if driver is None:
            click.echo("No driver available for %s" % provider)
            return

        click.echo("Driver for %s is %s" % (provider, str(driver)))
        di = driver(app.provider.username, app.provider.password)
        r = di.uninstall_app(appid)
        if r is None:
            click.echo("Error during app uninstall")
            return

        app.delete_instance()
        app.save()
    except Exception as ex:
        click.echo("Error: %s" % str(ex))


@app.command(help="Get application information")
@click.option('--appid', required=True, prompt=True)
def info(appid):
    try:
        app = Application.get(Application.appid == appid)
    except Exception as ex:
        click.echo("Error getting application info for %s" %  appid)
        click.echo("Try refreshing your config database <paascli refresh>")
        app = None
        return

    try:
        d = DriverManager.getInstance()
        driver = d.find_driver(app.provider.providername)
        if driver is None:
            click.echo("No driver available for %s" % provider)
            return

        click.echo("Driver for %s is %s" % (app.provider.providername, str(driver)))
        di = driver(app.provider.username, app.provider.password)
        r = di.get_app_info(appid)
        if r is None:
            click.echo("Error retrieving app info")
            return
        click.echo(json.dumps(r.json(), indent=2))

    except Exception as ex:
        click.echo("Error: %s" % str(ex))


@app.command(help="Start application")
@click.option('--appid', required=True, prompt=True)
def start(appid):

    try:
        app = Application.get(Application.appid == appid)
    except Exception as ex:
        click.echo("Error getting application info for %s" %  appid)
        click.echo("Try refreshing your config database <paascli refresh>")
        app = None
        return

    try:
        d = DriverManager.getInstance()
        driver = d.find_driver(app.provider.providername)
        if driver is None:
            click.echo("No driver available for %s" % provider)
            return

        click.echo("Driver for %s is %s" % (app.provider.providername, str(driver)))
        di = driver(app.provider.username, app.provider.password)
        r = di.start_app(appid)
        if r is None:
            click.echo("Error retrieving app info")
            return
        click.echo("Successfully started")

    except Exception as ex:
        click.echo("Error: %s" % str(ex))

@app.command(help="Stop application")
@click.option('--appid', required=True, prompt=True)
def stop(appid):

    try:
        app = Application.get(Application.appid == appid)
    except Exception as ex:
        click.echo("Error getting application info for %s" %  appid)
        click.echo("Try refreshing your config database <paascli refresh>")
        app = None
        return

    try:
        d = DriverManager.getInstance()
        provider = app.provider.providername
        driver = d.find_driver(provider)
        if driver is None:
            click.echo("No driver available for %s" % provider)
            return

        click.echo("Driver for %s is %s" % (provider, str(driver)))
        di = driver(app.provider.username, app.provider.password)
        r = di.stop_app(appid)
        if r is None:
            click.echo("Error retrieving app info")
            return
        click.echo("Successfully stopped")

    except Exception as ex:
        click.echo("Error: %s" % str(ex))


@app.command(help="List all installed applications")
@click.option('--provider')
def list(provider):

    click.echo("Listing all applications")
    if provider is None:
        for a in Application.select():
            click.echo("%s" % str(a))
    else:
        for a in Application.select().join(Provider).where(Provider.providername == provider):
            click.echo("%s" % str(a))
