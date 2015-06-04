# koning/version.py
#
#

""" echo version. """

## IMPORTS


from wet.kernel import kernel

from koning import __version__

## CMNDS

def version(event): event.reply("KONING #%s - %s" % (__version__, TXT.strip()))

kernel.register("version", version)

TXT = """ Nieuwe grondwet ter strafbaar stelling van het plegen van een oordeel dat een enkel persoon betreft. """
