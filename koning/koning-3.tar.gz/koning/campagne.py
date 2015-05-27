# koning/campagne.py
#
#

""" the thing to resolve. """

## IMPORTS

from wet.utils.time import a_time, nr_days, elapsed_days
from wet.clock import Repeater
from wet.kernel import kernel
from wet.thing import Thing

## basic imports

import datetime
import random
import time

## SuicideWarnLoop

names = ["crisis", "verwijs", "uitstroom", "politie", "geslaagd"]

crisisjaar = 150000
verwijsjaar = crisisjaar * 0.85
uitstroomjaar = crisisjaar * 0.05
opnamejaar = crisisjaar * 0.15
suicidejaar = 1854
crisisdag = crisisjaar / 365.0
crisisuur = crisisdag / 24.0
crisismin = crisisuur / 60.0
verwijsdag = verwijsjaar / 365.0
verwijsuur = verwijsdag / 24.0
verwijsmin = verwijsuur / 60.0
uitstroomdag = uitstroomjaar / 365.0
uitstroomuur = uitstroomdag / 24.0
uitstroommin = uitstroomuur / 60.0
opnamedag = opnamejaar / 365.0
opnameuur = opnamedag / 24.0
opnamemin = opnameuur / 60.0
suicidedag = suicidejaar / 365.0
suicideuur = suicidedag / 24.0
suicidemin = suicideuur / 60.0
counter = 0
startdate = "2015-01-01 00:00:00"
starttime = a_time(startdate)

bron = "https://www.113online.nl/informatie/113online%2B/cijfers-over-zelfmoord"
url = "http://pypi.python.org/pypi/koning"
source = "http://pikacode.com/bthate/wet"
fact = "http://tuchtrecht.overheid.nl/zoeken/resultaat/uitspraak/2014/ECLI_NL_TGZRAMS_2014_94?zaaknummer=2013%2F221&Pagina=1&ItemIndex=1"
tiny = "http://tinyurl.com/tuchtfact"

prevcrisis = 0
prevverwijs = 0
prevuitstroom = 0
prevopname = 0
prevgeslaagd = 0

lastcrisis = 0
lastverwijs = 0
lastuitstroom = 0
lastopname = 0
lastsuicide = 0

def ltag(*args, **kwargs):
    l = []
    while 1:
        c = random.choice(tags)
        if c not in l: l.append(c)
        if len(l) == args[0]: break
    return " ".join(l)

def crisis(*args, **kwargs):
    time_diff = time.time() - starttime
    aantalmin = time_diff / 60.0 
    crisis = int(aantalmin * crisismin)
    time_diff = float(time.time() - starttime)
    elapsed = elapsed_days(time_diff)
    lastcrisis = 0
    if crisis > lastcrisis:
        txt = "CRISIS %s - %s #ggz #wet (%s/dag)" % (crisis, url, int(crisisdag))
        lastcrisis = crisis
        kernel.announce(txt)

kernel.register("campagne.crisis", crisis)

def verwijs(*args, **kwargs):
    time_diff = time.time() - starttime
    aantalmin = time_diff / 60.0 
    verwijs = int(aantalmin * verwijsmin)
    time_diff = float(time.time() - starttime)
    elapsed = elapsed_days(time_diff)
    lastverwijs = 0
    if verwijs > lastverwijs:
        txt = "VERWIJS %s - %s #ggz #wet (%s/dag)" % (verwijs, url, int(verwijsdag))
        lastverwijs = verwijs
        kernel.announce(txt)

kernel.register("campagne.verwijs", verwijs)

def uitstroom(*args, **kwargs):
    time_diff = time.time() - starttime
    aantalmin = time_diff / 60.0 
    uitstroom = int(aantalmin * uitstroommin)
    time_diff = float(time.time() - starttime)
    elapsed = elapsed_days(time_diff)
    lastuitstroom = 0
    if uitstroom > lastuitstroom:
        txt = "UITSTROOM %s - %s #ggz #wet (%s/dag)" % (uitstroom, url, int(uitstroomdag))
        uitstroompoging = uitstroom
        kernel.announce(txt)

kernel.register("campagne.uitstroom", uitstroom)

def opname(*args, **kwargs):
    time_diff = time.time() - starttime
    aantalmin = time_diff / 60.0 
    opname = int(aantalmin * opnamemin)
    time_diff = float(time.time() - starttime)
    elapsed = elapsed_days(time_diff)
    lastopname = 0
    if opname > lastopname:
        txt = "OPNAME %s - %s #ggz #wet (%s/dag)" % (opname, url, int(opnamedag))
        lastopname = opname
        kernel.announce(txt)

kernel.register("campagne.opname", opname)

def totaal(*args, **kwargs):
    time_diff = time.time() - starttime
    aantalmin = time_diff / 60.0 
    suicide = int(aantalmin * suicidemin)
    crisis = int(aantalmin * crisismin)
    verwijs = int(aantalmin * verwijsmin)
    uitstroom = int(aantalmin * uitstroommin)
    opname = int(aantalmin * opnamemin)
    time_diff = float(time.time() - starttime)
    elapsed = elapsed_days(time_diff)
    lastcrisis = 0
    if crisis > lastcrisis:
        txt = "CRISIS %s - VERWIJS %s (%s/dag) UITSTROOM %s (%s/dag) OPNAME %s (%s/dag) SUICIDE %s (%s/dag) - %s #ggz #wet (%s)" % (crisis, verwijs, int(verwijsdag), uitstroom, int(uitstroomdag), opname, int(opnamedag), suicide, int(suicidedag), url, elapsed_days(time_diff))
        lastcrisis = crisis
        kernel.announce(txt)

kernel.register("campagne.totaal", totaal)

## Campagne class

class CRISIS(Repeater): pass
class VERWIJS(Repeater): pass
class UITSTROOM(Repeater): pass
class OPNAME(Repeater): pass
class SUICIDE(Repeater): pass
class TOTAAL(Repeater): pass

## campagne init

def init(*args, **kwargs):
    todo = TOTAAL(totaal, 60 * 60 * 24 / suicidedag)
    kernel.put(todo.start)
