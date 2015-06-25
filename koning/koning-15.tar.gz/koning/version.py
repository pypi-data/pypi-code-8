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

TXT = """ Recht op leven. Recht op Vrijheid en Veiligheid. """
