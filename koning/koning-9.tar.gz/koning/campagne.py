# koning/campagne.py
#
#

""" the thing to resolve. """

## IMPORTS

from wet.utils.time import a_time, nr_days, elapsed_days, today
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
politiejaar = 0.15 * crisisjaar 
hapjaar = 0.40 * crisisjaar
ketenjaar = 0.45 * crisisjaar
verwijsjaar = crisisjaar * 0.85
uitstroomjaar = crisisjaar * 0.05
opnamejaar = crisisjaar * 0.15
suicidejaar = 1854
politiedag = politiejaar / 365.0
politieuur = politiedag / 24.0
politiemin = politieuur / 60.0
hapdag = hapjaar / 365.0
hapuur = hapdag / 24.0
hapmin = hapuur / 60.0
ketendag = ketenjaar / 365.0
ketenuur = ketendag / 24.0
ketenmin = ketenuur / 60.0
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

def heden(*args, **kwargs):
    time_diff = time.time() - today()
    aantalmin = time_diff/ 60
    crisis = int(aantalmin * crisismin)
    politie = int(aantalmin * politiemin)
    hap = int(aantalmin * hapmin)
    keten = int(aantalmin * ketenmin)
    verwijs = int(aantalmin * verwijsmin)
    uitstroom = int(aantalmin * uitstroommin)
    opname = int(aantalmin * opnamemin)
    suicide = int(aantalmin * suicidemin)
    elapsed = elapsed_days(time_diff)
    lastcrisis = 0
    if crisis > lastcrisis:
        txt = "CRISIS %s POLITIE %s HAP %s KETEN %s - VERWIJS %s UITSTROOM %s OPNAME %s SUICIDE %s %s %s" % (crisis, politie, hap, keten, verwijs, uitstroom, opname, suicide, url, elapsed)
        lastcrisis = crisis
        kernel.announce(txt)

kernel.register("campagne.heden",heden)

## Campagne class

class CRISIS(Repeater): pass
class VERWIJS(Repeater): pass
class UITSTROOM(Repeater): pass
class OPNAME(Repeater): pass
class SUICIDE(Repeater): pass
class CRISIS(Repeater): pass

## campagne init

def init(*args, **kwargs):
    todo = CRISIS(heden, int(60 * 60 * 24 / crisisdag))
    kernel.put(todo.start)
