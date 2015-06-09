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

## DEFINES

names = ["crisis", "politie", "hap", "keten", "followup", "uitstroom", "opname", "suicide"]
counter = 0
startdate = "2015-01-01 0:0:0"
starttime = a_time(startdate)

bron = "https://www.113online.nl/informatie/113online%2B/cijfers-over-zelfmoord"
url = "http://pypi.python.org/pypi/koning"
source = "http://pikacode.com/bthate/wet"
fact = "http://tuchtrecht.overheid.nl/zoeken/resultaat/uitspraak/2014/ECLI_NL_TGZRAMS_2014_94?zaaknummer=2013%2F221&Pagina=1&ItemIndex=1"
tiny = "http://tinyurl.com/tuchtfact"

## AANTAL

jaar = Thing()
jaar.crisis = 150000
jaar.politie = int(0.15 * jaar.crisis) 
jaar.hap = int(0.40 * jaar.crisis)
jaar.keten = int(0.45 * jaar.crisis)
jaar.followup = int(jaar.crisis * 0.85)
jaar.uitstroom = int(jaar.crisis * 0.05)
jaar.opname = int(jaar.crisis * 0.10)
jaar.suicide = 1854

# AANTAL SECONDEN

seconds = Thing()
seconds.politie = int(365 * 24 * 60 * 60 / jaar.politie)
seconds.hap = int(365 * 24 * 60 * 60 / jaar.hap)
seconds.keten = int(365  * 24 * 60 * 60 / jaar.keten)
seconds.crisis = int(365 * 24 * 60 * 60 / jaar.crisis)
seconds.followup = int(365 * 24 * 60 * 60 / jaar.followup) 
seconds.uitstroom = int(365 * 24 * 60 * 60 / jaar.uitstroom)
seconds.opname = int(365 * 24 * 60 * 60 / jaar.opname)
seconds.suicide = int(365 * 24 * 60 * 60 / jaar.suicide)

def until(*args, **kwargs):
    delta = args[0]
    next = Thing()
    next.crisis = seconds.crisis - int(delta % seconds.crisis)
    next.politie = seconds.politie - int(delta % seconds.politie)
    next.hap = seconds.hap - int(delta % seconds.hap)
    next.keten = seconds.keten - int(delta % seconds.keten)
    next.followup = seconds.followup - int(delta % seconds.followup)
    next.uitstroom = seconds.uitstroom - int(delta % seconds.uitstroom)
    next.opname = seconds.opname - int(delta % seconds.opname)
    next.suicide = seconds.suicide - int(delta % seconds.suicide)
    return next

def value(*args, **kwargs):
    delta = args[0]
    value = Thing()
    value.crisis = int(delta / seconds.crisis)
    value.politie = int(delta / seconds.politie)
    value.hap = int(delta / seconds.hap)
    value.keten = int(delta / seconds.keten)
    value.followup = int(delta / seconds.followup)
    value.uitstroom = int(delta / seconds.uitstroom)
    value.opname = int(delta / seconds.opname)
    value.suicide = int(delta / seconds.suicide)
    return value

def ltag(*args, **kwargs):
    l = []
    while 1:
        c = random.choice(tags)
        if c not in l: l.append(c)
        if len(l) == args[0]: break
    return " ".join(l)


def delta(*args, **kwargs):
    txt = "CRISIS/%s " % elapsed_days(seconds.crisis)
    txt += "POLITIE/%s " % elapsed_days(seconds.politie)
    txt += "HAP/%s " % elapsed_days(seconds.hap)
    txt += "KETEN/%s " % elapsed_days(seconds.keten)
    txt += "==> "
    txt += "FOLLOWUP/%s " % elapsed_days(seconds.followup)
    txt += "UITSTROOM/%s " % elapsed_days(seconds.uitstroom)
    txt += "OPNAME/%s " % elapsed_days(seconds.opname)
    txt += "SUICIDE/%s " % elapsed_days(seconds.suicide)
    kernel.announce(txt.strip())

kernel.register("campagne.delta", delta)

def crisis(*args, **kwargs):
    delta = time.time() - starttime
    values = value(delta)
    txt = "CRISIS/%d " % values.crisis
    txt += "POLITIE/%d " % values.politie
    txt += "HAP/%d " % values.hap
    txt += "KETEN/%d " % values.keten
    txt += "==> "
    txt += "FOLLOWUP/%d " % values.followup
    txt += "UITSTROOM/%d " % values.uitstroom
    txt += "OPNAME/%d " % values.opname
    txt += "SUICIDE/%d " % values.suicide
    txt += "(%s)" % elapsed_days(delta)
    kernel.announce(txt.strip())

kernel.register("campagne.crisis", crisis)

def do_next(*args, **kwargs):
    delta = time.time() - starttime
    next = until(delta)
    txt = "CRISIS/%s " % elapsed_days(next.crisis)
    txt += "POLITIE/%s " % elapsed_days(next.politie)
    txt += "HAP/%s " % elapsed_days(next.hap)
    txt += "KETEN/%s " % elapsed_days(next.keten)
    txt += "==> "
    txt += "FOLLOWUP/%s " % elapsed_days(next.followup)
    txt += "UITSTROOM/%s " % elapsed_days(next.uitstroom)
    txt += "OPNAME/%s " % elapsed_days(next.opname)
    txt += "SUICIDE/%s " % elapsed_days(next.suicide)
    txt += "(%s)" % elapsed_days(delta)
    kernel.announce(txt.strip())

kernel.register("campagne.next", do_next)

def campagne(*args, **kwargs):
    polltime = args[0]
    delta = time.time() - starttime
    txt = ""
    values = value(delta)
    next = until(delta)
    for name in names:
         if int(next.get(name) / polltime) % values.get(name) == 0:
            val = values.get(name, None)
            if val: txt += " %s/%d" % (name.upper(), int(val))
            if txt: txt += " (%s)" % elapsed_days(seconds.get(name))
    if txt: kernel.announce(txt.strip())

## campagne init

def init(*args, **kwargs):
    todo = Repeater(campagne, 3600)
    todo = Repeater(crisis, 300)
    kernel.put(todo.start)
