# koning/version.py
#
#

""" echo version. """

## IMPORTS


from kern.kernel import kernel

from koning import __version__

## CMNDS

def version(event): event.reply("KONING #%s - %s" % (__version__, TXT.strip()))

kernel.register("version", version)

TXT = """ Recht op leven. We moeten de Koning zien te overtuigen tot het strafbaar stellen van het toedienen van antipsychotica. Antipsychotica zijn dodelijk. """
