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
from mapshop.management.commands.utils import *

#logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        print 'start'
        
        ProductImages.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Order.objects.all().delete()
        Client.objects.all().delete()
        User.objects.all().exclude(username='admin').delete()
        l = [ 'food','slippers']
        
        for i in l:
            o = Category()
            o.name = i
            o.save()
            cnt = 0
            for n in range(10):
                cnt = cnt  + 1 
                p = Product()
                p.category = o
                p.price = n
                p.rate = randint(0,90)
                p.name = 'Product %s %s' % (n,o.name)
                p.description = u'Описание продукта %s из категории %s у которого рейтинг %s' % (p.name,o.name,p.rate)
                p.save()
                for im in range(3):
                    path = 'fixture/test.jpg'
                    #import pdb; pdb.set_trace()
                    name = 'test.jpg' 
                    f = open(path, 'r')
                    file = File(f)
                    im = ProductImages()
                    im.product = p
                    im.image.save(name,file)
                    im.save()
                    print 'process with image %s' % im
                print 'process with %s' % n
        
        for u in ['dima','viktor','alex']:
            client = create_user(u)
            product = Product.objects.get(pk=1)
            create_preloader(client, product)
            
        #o = Order()
        #o.save()
        #print 'order was created'

      

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

       
