# -*- coding: utf-8 -*-

"""Importer posnr fra postens datafil (p.t. på
   http://epab.posten.no/Norsk/Nedlasting/NedlastingMeny1.htm).

   Filene endrer seg litt fra år til år, så denne importen må som regel
   justeres for hver import.

   Postnummerregister_ANSI.txt -filen ser ut til å være den vi ønsker.
"""


import codecs
from django import template
from .models import Kommune, PostSted


DATAFILE = 'data/postnummerregister_ansi.txt'
ENCODING = 'cp1252'

def split_line(line):
    return [item.strip() for item in line.split('\t')]

def readfile():
    """Yield all postnr from DATAFILE that we currently do not have in db.
    """
    #current = set(p.postnummer for p in PostSted.objects.all())

    for line in codecs.open(DATAFILE, encoding=ENCODING):
        postnr, sted, kkode, knavn, _ = split_line(line)
        yield postnr, sted, kkode, knavn


def insert(postnr, sted, kkode, knavn):
    "Insert the values in db (guaranteed to be new)."
    p, _ = PostSted.objects.get_or_create(postnummer=postnr)
    p.poststed = sted
    p.kommune, _ = Kommune.objects.get_or_create(kode=kkode, navn=knavn)
    p.save()
    print p.postnummer


def create_posnrcache_py():
    postnrs = [int(p) for p in
               sorted(set(p.postnummer for p in PostSted.objects.all()))]
    t = template.Template(open('postnrcache.pytempl').read().decode('u8'))
    
    fp = open('postnrcache.py', 'w')
    fp.write(unicode(t.render(template.Context(locals()))).encode('u8'))
    fp.close()
    

def main():
    "main()"
    print 'starting insert...'
    for i, v in enumerate(readfile()):
        print i,
        insert(*v)
    print 'finished inserting.'
    print 'starting postnrcache.py creation...'
    create_posnrcache_py()
    print 'finished.'


if __name__ == "__main__":
    main()
    #pass
