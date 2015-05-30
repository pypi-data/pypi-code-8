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

TXT = """ Wetsvoorstel tot het strafbaar maken van het toedienen van antipsychotica. """
