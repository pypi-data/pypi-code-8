# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from mapshop.forms import ProductFilterForm
from mapshop.models import Category, Product, Kiosk, Order, Client, get_client_or_create
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.http import HttpResponse

@csrf_exempt
def product_edit(request):
    status = '0'
    message = 'Ok'
    indata = simplejson.loads(request.body)

    try:
        product = Product.objects.get(pk = indata['product_id'])
    except:
        status = '1'
        message = 'Could not find product by ID'   

    try:
        av = indata['ammount']
        product.ammount = av
        message = 'Product %s setting ammount in value %s !!!' % (product,av)
        product.save()
    except:
        pass
        
    out = {
        'status': status,
        'message': message,
    }
    outdata = simplejson.dumps(out)
    return HttpResponse(outdata, mimetype='application/json')



@csrf_exempt
def product_bye(request):
    indata = simplejson.loads(request.body)
    print 'bye %s ammount %s ' % (indata['product_id'], indata['ammount'])
    out = {
        'status': 0,
        'message': 'Ok',
    }
    outdata = simplejson.dumps(out)
    return HttpResponse(outdata, mimetype='application/json')

