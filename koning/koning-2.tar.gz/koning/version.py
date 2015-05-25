# koning/version.py
#
#

""" echo version. """

## IMPORTS


from wet.kernel import kernel

from koning import __version__

## CMNDS

def version(event): event.reply("KONING #%s - %s" % (__version__, TXT))

kernel.register("version", version)

TXT = """
Antipsychotica zijn dodelijke medicijnen en daarom is verpleging een
noodzaak. Behandeling met antipsychotica zonder de noodzakelijke verpleging
is maken van omstandigheden die suicide in de hand werken.

(F)ACT bied niet de noodzakelijke verpleging die behandeling met
antipsychotica verantwoord maken.

1) verpleging naar gelang de situatie - meer zorg naarmate de situatie erger is, is niet preventief.
2) niet 7 x 24 uurs verpleging - in het weekend en avonduren niet aanwezig  
3) psychiater is niet op de hoogte van de situatie van de patient
4) behandelovereenkomsten zijn niet volledig
5) zonder bedden geen snelle terugbrenging naar ziekenhuis mogelijk.
"""
