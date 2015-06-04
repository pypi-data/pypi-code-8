# koning/campagne.py
#
#

""" the thing to resolve. """

## IMPORTS

from wet.utils.time import a_time, nr_days, elapsed_days, today
from wet.clock import Repeater
from wet.kernel import kernel
from wet.thing import Thing

import datetime
import random
import time

## AANTAL

crisisjaar = 150000
politiejaar = int(0.15 * crisisjaar) 
hapjaar = int(0.40 * crisisjaar)
ketenjaar = int(0.45 * crisisjaar)
followupjaar = int(crisisjaar * 0.85)
uitstroomjaar = int(crisisjaar * 0.05)
opnamejaar = int(crisisjaar * 0.10)
suicidejaar = 1854

# AANTAL SECONDEN

politiesec = 365 * 24 * 60 * 60 / politiejaar
hapsec = 365 * 24 * 60 * 60 / hapjaar
ketensec = 365  * 24 * 60 * 60 / ketenjaar
crisissec = 365 * 24 * 60 * 60 / crisisjaar
followupsec = 365 * 24 * 60 * 60 / followupjaar 
uitstroomsec = 365 * 24 * 60 * 60 / uitstroomjaar
opnamesec = 365 * 24 * 60 * 60 / opnamejaar
suicidesec = 365 * 24 * 60 * 60 / suicidejaar
counter = 0
startdate = "2012-09-13 00:00:00"
starttime = a_time(startdate)

bron = "https://www.113online.nl/informatie/113online%2B/cijfers-over-zelfmoord"
url = "http://pypi.python.org/pypi/koning"
source = "http://pikacode.com/bthate/wet"
fact = "http://tuchtrecht.overheid.nl/zoeken/resultaat/uitspraak/2014/ECLI_NL_TGZRAMS_2014_94?zaaknummer=2013%2F221&Pagina=1&ItemIndex=1"
tiny = "http://tinyurl.com/tuchtfact"

def ltag(*args, **kwargs):
    l = []
    while 1:
        c = random.choice(tags)
        if c not in l: l.append(c)
        if len(l) == args[0]: break
    return " ".join(l)

def crisis(*args, **kwargs):
    delta = time.time() - starttime
    crisis = delta / crisissec
    nextcrisis = delta % crisissec
    politie = delta / politiesec
    nextpolitie = delta % politiesec
    hap = delta / hapsec
    nexthap = delta % hapsec
    keten = delta / ketensec
    nextketen = delta % ketensec
    followup = delta / followupsec
    nextfollowup = delta % followupsec
    uitstroom = delta / uitstroomsec
    nextuitstroom = delta % uitstroomsec
    opname = delta / opnamesec
    nextopname = delta % opnamesec
    suicide = delta / suicidesec
    nextsuicide = delta % suicidesec
    txt = "CRISIS/%s/%d " % (elapsed_days(crisissec), crisis)
    txt += "POLITIE/%s/%d " % (elapsed_days(politiesec), politie)
    txt += "HAP/%s/%d " % (elapsed_days(hapsec), hap)
    txt += "KETEN/%s/%d " % (elapsed_days(ketensec), keten)
    txt += "==> "
    txt += "FOLLOWUP/%s/%d " % (elapsed_days(followupsec), followup)
    txt += "UITSTROOM/%s/%d " % (elapsed_days(uitstroomsec), uitstroom)
    txt += "OPNAME/%s/%d " % (elapsed_days(opnamesec), opname)
    txt += "SUICIDE/%s/%d " % (elapsed_days(suicidesec), suicide)
    kernel.announce(txt.strip())

kernel.register("campagne.crisis", crisis)

def until(*args, **kwargs):
    delta = time.time() - starttime
    crisis = delta / crisissec
    nextcrisis = delta % crisissec
    politie = delta / politiesec
    nextpolitie = delta % politiesec
    hap = delta / hapsec
    nexthap = delta % hapsec
    keten = delta / ketensec
    nextketen = delta % ketensec
    followup = delta / followupsec
    nextfollowup = delta % followupsec
    uitstroom = delta / uitstroomsec
    nextuitstroom = delta % uitstroomsec
    opname = delta / opnamesec
    nextopname = delta % opnamesec
    suicide = delta / suicidesec
    nextsuicide = delta % suicidesec
    txt = "CRISIS/%s " % elapsed_days(crisissec - nextcrisis)
    txt += "POLITIE/%s " % elapsed_days(politiesec - nextpolitie)
    txt += "HAP/%s " % elapsed_days(hapsec - nexthap)
    txt += "KETEN/%s " % elapsed_days(ketensec - nextketen)
    txt += "==> "
    txt += "FOLLOWUP/%s " % elapsed_days(followupsec - nextfollowup)
    txt += "UITSTROOM/%s " % elapsed_days(uitstroomsec - nextuitstroom)
    txt += "OPNAME/%s " % elapsed_days(opnamesec - nextopname)
    txt += "SUICIDE/%s " % elapsed_days(suicidesec - nextsuicide)
    kernel.announce(txt.strip())

kernel.register("campagne.until", until)

def polling(*args, **kwargs):
    delta = time.time() - starttime
    crisis = delta / crisissec 
    nextcrisis = delta % crisissec
    politie = delta / politiesec 
    nextpolitie = delta % politiesec
    hap = delta / hapsec
    nexthap = delta % hapsec
    keten = delta / ketensec
    nextketen = delta % ketensec
    followup = delta / followupsec 
    nextfollowup = delta % followupsec
    uitstroom = delta / uitstroomsec
    nextuitstroom = delta % uitstroomsec
    opname = delta / opnamesec
    nextopname = delta % opnamesec
    suicide = delta / suicidesec
    nextsuicide = delta % suicidesec
    txt = ""
    #if int(crisissec - nextcrisis) / 60 % crisissec < 1: txt = "CRISIS %s " % int(crisis)
    if int(politiesec - nextpolitie) / 60 % politiesec < 1: txt += "POLITIE %d " % int(politie)
    if int(hapsec - nexthap) / 60 % hapsec < 1: txt += "HAP %d " % int(hap)
    if int(ketensec - nextketen) / 60 % ketensec < 1: txt += "KETEN %d " % int(keten)
    if int(followupsec - nextfollowup) / 60 % followupsec  < 1 : txt += "FOLLOWUP %d " % int(followup)
    if int(uitstroomsec - nextuitstroom) / 60 % uitstroomsec < 1:txt += "UITSTROOM %d " % int(uitstroom)
    if int(opnamesec - nextopname) / 60 % opnamesec < 1: txt += "OPNAME %d " % int(opname)
    if int(suicidesec - nextsuicide) / 60 % suicidesec < 1: txt += "SUICIDE %d " % int(suicide)
    if txt: kernel.announce(txt.strip())

kernel.register("campagne.polling", polling)

## campagne init

def init(*args, **kwargs):
    todo = Repeater(polling, 60)
    kernel.put(todo.start)
