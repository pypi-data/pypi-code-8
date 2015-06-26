# koning/campagne.py
#
#

""" the thing to resolve. """

## IMPORTS

from wet.utils.time import a_time, nr_days, elapsed_days, today
from wet.clock import Repeater
from wet.kernel import kernel
from wet.thing import Thing

from koning.gemeenten import gemeenten_txt

import datetime
import random
import time

## DEFINES

names_in = ["politie", "hap", "keten"]
names_out = ["followup", "uitstroom", "opname", "suicide"]
counter = 0
startdate = "2015-01-01 0:0:0"
starttime = a_time(startdate)
crisis = 150000
suicide = 1854

urls = {
        "followup": "http://pypi.python.org/pypi/huisarts",
        "uitstroom": "http://pypi.python.org/pypi/huisarts",
        "opname": "http://pypi.python.org/pypi/huisarts",
        "suicide": "http://pypi.python.org/pypi/huisarts",
        "keten": "http://pypi.python.org/pypi/gemeente",
        "hap": "http://pypi.python.org/pypi/minister",
        "politie": "http://pypi.python.org/pypi/koning"
       }

## TAGS

tags = Thing()
tags.politie = "#broodjepindakaas"
tags.hap = "#triade"
tags.keten = "#wetverplichteggz"
tags.followup = "#prettigweekend"
tags.uitstroom = "#jammerdan"
tags.opname = "#geenbedvoorjou"
tags.suicide = "#gebodenvrucht"

## AANTAL

jaar = Thing()
jaar.politie = 0.15 * crisis
jaar.hap = 0.40 * crisis
jaar.keten = 0.45 * crisis
jaar.followup = crisis * 0.85
jaar.uitstroom = crisis * 0.05
jaar.opname = crisis * 0.10

# AANTAL SECONDEN

seconds = Thing()
seconds.politie = int(365 * 24 * 60 * 60 / jaar.politie)
seconds.hap = int(365 * 24 * 60 * 60 / jaar.hap)
seconds.keten = int(365  * 24 * 60 * 60 / jaar.keten)
seconds.followup = int(365 * 24 * 60 * 60 / jaar.followup) 
seconds.uitstroom = int(365 * 24 * 60 * 60 / jaar.uitstroom)
seconds.opname = int(365 * 24 * 60 * 60 / jaar.opname)
seconds.suicide = int(365 * 24 * 60 * 60 / suicide)
seconds.crisis = int(365 * 24 * 60 * 60 / crisis)

## HELPERS

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

def values(*args, **kwargs):
    delta = args[0]
    value = Thing()
    value.politie = int(delta / seconds.politie)
    value.hap = int(delta / seconds.hap)
    value.keten = int(delta / seconds.keten)
    value.followup = int(delta / seconds.followup)
    value.uitstroom = int(delta / seconds.uitstroom)
    value.opname = int(delta / seconds.opname)
    value.suicide = int(delta / seconds.suicide)
    value.crisis = int(delta / seconds.crisis)
    return value

def lowest(*args, **kwargs):
    delta = args[0]
    low = 100000000000000
    res = ""
    for name in names_in:
        nr = seconds.get(name)
        remaining = nr - delta % nr
        if remaining < low: res = name ; low = remaining
    return res

## COMMANDS

def do_volgende(event):
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
    event.reply(txt.strip())

kernel.register("volgende", do_volgende)

def do_oordeel(event):
    delta = time.time() - starttime
    val = values(delta)
    txt = "CRISIS/%s " % val.crisis
    txt += "POLITIE/%s " % val.politie
    txt += "HAP/%s " % val.hap
    txt += "KETEN/%s " % val.keten
    txt += "==> "
    txt += "FOLLOWUP/%s " % val.followup
    txt += "UITSTROOM/%s " % val.uitstroom
    txt += "OPNAME/%s " % val.opname
    txt += "SUICIDE/%s " % val.suicide
    txt += "(%s)" % elapsed_days(delta)
    event.reply(txt.strip())

kernel.register("oordeel", do_oordeel)

def do_alarm(event):
    delta = time.time() - starttime
    txt = "CRISIS/%s " % elapsed_days(seconds.crisis)
    txt += "POLITIE/%s " % elapsed_days(seconds.politie)
    txt += "HAP/%s " % elapsed_days(seconds.hap)
    txt += "KETEN/%s " % elapsed_days(seconds.keten)
    txt += "==> "
    txt += "FOLLOWUP/%s " % elapsed_days(seconds.followup)
    txt += "UITSTROOM/%s " % elapsed_days(seconds.uitstroom)
    txt += "OPNAME/%s " % elapsed_days(seconds.opname)
    txt += "SUICIDE/%s " % elapsed_days(seconds.suicide)
    txt += "(%s)" % elapsed_days(delta)
    event.reply(txt.strip())

kernel.register("alarm", do_alarm)

## CHECKER

def oordeel(event):
    delta = time.time() - starttime
    next = until(delta)
    for name in names_out:
        nr = int(delta / seconds.get(name))
        txt = "%s %s/%d (%s) %s %s" % (time.ctime(time.time()), name.upper(), nr, elapsed_days(next.get(name)), urls.get(name, ""), tags.get(name)) 
        event.reply(txt.strip())

kernel.register("campagne.oordeel", oordeel)

def alarm(event):
    delta = time.time() - starttime
    next = until(delta)
    for name in names_in:
        nr = int(delta / seconds.get(name))
        txt = "%s %s/%d (%s) %s %s" % (time.ctime(time.time()), name.upper(), nr, elapsed_days(next.get(name)), urls.get(name, ""), tags.get(name)) 
        if name in names_in: txt += " - %s" % random.choice(gemeenten_txt.split("\n"))
        event.reply(txt.strip())

kernel.register("campagne.alarm", alarm)

def beoordeling(*args, **kwargs):
    delta = time.time() - starttime
    next = until(delta)
    for name in names_out:
        nr = int(delta / seconds.get(name))
        if int(seconds.get(name) - delta) % seconds.get(name) == 0: 
            txt = "%s %s/%d (%s) %s %s" % (time.ctime(time.time()), name.upper(), nr, elapsed_days(next.get(name)), urls.get(name, ""), tags.get(name)) 
            kernel.announce(txt.strip())

def alarm(*args, **kwargs):
    delta = time.time() - starttime
    next = until(delta)
    for name in names_in:
        nr = int(delta / seconds.get(name))
        if int(seconds.get(name) - delta) % seconds.get(name) == 0: 
            txt = "%s %s/%d (%s) %s %s" % (time.ctime(time.time()), name.upper(), nr, elapsed_days(next.get(name)), urls.get(name, ""), tags.get(name)) 
            if name in names_in: txt += " - %s" % random.choice(gemeenten_txt.split("\n"))
            kernel.announce(txt.strip())

## INIT

def init(*args, **kwargs):
    todo = Repeater(alarm, 1)
    #todo = Repeater(beoordeling, 1)
    kernel.put(todo.start)
