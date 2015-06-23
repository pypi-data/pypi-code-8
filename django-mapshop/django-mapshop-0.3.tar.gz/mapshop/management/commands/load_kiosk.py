# -*- coding: utf-8 -*-
import logging
from optparse import make_option
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from mapshop.models import Category, Product, ProductImages, Kiosk , Order, Client
from django.core.files import File
from random import randint
import csv
from django.contrib.auth.models import User

#logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        print 'start'
        Kiosk.objects.all().delete()
        input_file = open("kiosk.csv", "rb")
        rdr = csv.DictReader(input_file, delimiter=';', fieldnames=['mnemonic', 'name', 'address','latitude','longitude'])
        for rec in rdr:
            #try:
            k = Kiosk()
            k.mnemonic = rec['mnemonic']
            k.name = rec['name']
            k.address = rec['address']
            k.latitude = rec['latitude']
            k.longitude = rec['longitude']
            path = 'fixture/kiosk.jpg'
            #import pdb; pdb.set_trace()
            name = 'kiosk.jpg'
            f = open(path, 'r')
            file = File(f)
            k.foto.save(name,file)
            k.save()
            #except:
            print 'kiosk....%s...done' % k.address
        input_file.close()
        print 'done'

'''
import tempfile
from django.core import files
lf = tempfile.NamedTemporaryFile()
for block in open('path','r'):
    if not block:
        break
    lf.write(block)
j.cover.save(file_name, files.File(lf))

'''

       
