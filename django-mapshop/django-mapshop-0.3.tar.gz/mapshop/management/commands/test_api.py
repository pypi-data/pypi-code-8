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
from termcolor import colored
import json
import requests
#logger = logging.getLogger(__name__)


    
    
    

class Command(BaseCommand):

    def handle(self, *args, **options):
        print colored('start test API', 'green', attrs=['reverse', 'blink'])
        product = Product.objects.get(pk=1)
        if product.ammount==0:
            av = '1'
        else:
            av = '0'
        data = {'product_id': '1', 'ammount': av}
        mess = '****request to change availability of %s to None' % product
        url = 'http://localhost:8008/api/product/edit'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        responce = requests.post(url, data=json.dumps(data), headers=headers).content
        print colored(responce, 'white')
        print colored('stop test API', 'red', attrs=['reverse', 'blink'])

        data = {'product_id': '1', 'ammount': '2'}
        mess = '****request to to bye '
        url = 'http://localhost:8008/api/product/bye'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        responce = requests.post(url, data=json.dumps(data), headers=headers).content
        print colored(responce, 'white')

       
