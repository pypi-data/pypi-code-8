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

    option_list = BaseCommand.option_list + (
        make_option('-c', dest='count', 
                    default="6", help="Count of record"),

        
    )

    def handle(self, *args, **options):
        cnt = int(options["count"])
        print 'start %s ' % cnt
        Product.objects.all().delete()
        Category.objects.all().delete()
        root = Category.objects.create(name=u'Каталог', parent=None)
        input_file = open("fixture/products.csv", "rb")
        rdr = csv.DictReader(input_file, delimiter=';', fieldnames=['id', 'name0', 'name', 'reference','ost','price', 'cat', 'subcat', 'photo'])
        i=0
        for rec in rdr:
            i = i + 1
            if cnt==i:
                break
            print '%s....product....%s...in process' % (i, rec['name'])
            try:
                cat = Category.objects.get(name=rec['cat'].decode('utf-8'))
            except:
    
                cat = Category.objects.create(name=rec['cat'].decode('utf-8'), parent=root)
            p = Product()
            p.name = rec['name'].decode('utf-8')
            p.category = cat
            p.price = rec['price'].decode('utf-8')
            p.save()
            #root.add_child_node()
        input_file.close()
        print 'done'


