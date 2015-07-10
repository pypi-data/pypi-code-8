# koning/version.py
#
#

""" echo version. """

## IMPORTS


from kern import kernel

from koning import __version__

## CMNDS

def version(event): event.reply("KONING #%s - %s" % (__version__, TXT.strip()))

kernel.register("version", version)

TXT = """ 3°. indien het misdrijf wordt gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen.  """
