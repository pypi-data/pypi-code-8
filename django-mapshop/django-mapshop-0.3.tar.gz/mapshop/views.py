# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from mapshop.forms import ProductFilterForm
from mapshop.models import Category, Product, Kiosk, Order, Client, get_client_or_create
from mapshop.forms import ClientForm
from django.http import HttpResponseRedirect


import django.dispatch
payment_done = django.dispatch.Signal(providing_args=["order_id"])



def home(request):
    context = {}
    payment_done.send(None,order_id=12)
    print 'my var %s ' % request.supervar
    return render_to_response('mapshop/home.html', context, RequestContext(request))


def product_list(request,slug='all'):
    u''' 
        Список товаров в категории (по умолчанию во всех категориях)
        при передаче параметров sort_price, sort_rate (up/down) сортируем.
    '''
    # initialization
    cur_rate_order = 'asc'
    cur_rate_price = 'asc'
    # get all products
    products = Product.objects.all()
    if slug=='all':
        title = 'Все товары'
        # select all categories 
        category_list = Category.objects.all()
    else:
        
        category =  Category.objects.get(name_slug=slug)
        title = 'Товары из категории "%s"' % category
        # select all categories excluding current
        category_list = Category.objects.all().exclude(name_slug=slug)
        # add filter
        products = products.filter(category=category)

    # handle with order
    try:
        #import pdb; pdb.set_trace()
        rate_order = request.GET['rate_order']
        if rate_order == 'desc':
            products = products.order_by('-rate')
            cur_rate_order = 'desc'
        else:
            products = products.order_by('rate')  
            cur_rate_order = 'asc'
    except:
        pass

    try:
        rate_price = request.GET['price_order']
        if rate_price == 'desc':
            products = products.order_by('-price')
            cur_rate_price = 'desc'
        else:
            products = products.order_by('price')  
            cur_rate_price = 'asc'
    except:
        pass

    #category = Course.objects.get(name=category_name)
    #Author.objects.order_by('-score')[:30]

    ''' avdey code
    filter_form = ProductFilterForm()
    if request.method == 'GET' and bool(request.GET):
        filter_form = ProductFilterForm(request.GET)
    data = dict(filter_form=filter_form)
    return render_to_response('product_list.html', data, RequestContext(request))
    '''

    context = {'title': title, 'category_list': category_list, 'product_list': products, 'cur_rate_order': cur_rate_order, 'cur_rate_price': cur_rate_price}
    return render_to_response('mapshop/product_list.html', context, RequestContext(request))



def product_detail(request,slug):
    u''' 
        Детальная информация о товаре
    '''
    product = get_object_or_404(Product,name_slug=slug) 
    similar = Product.objects.filter(category=product.category).order_by('-rate')[0:20]
    context = {'p': product, 'similar': similar}
    return render_to_response('mapshop/product_detail.html', context, RequestContext(request))

def kiosk_list(request,order_id=0):
    u''' 
        Отображение всех киосков 
    '''
    kiosk_list = Kiosk.objects.all()
    #try:
    order = Order.objects.get(pk=order_id)
    title = u'Выбор киоска для заказа № %s' % order_id
    #except:
    #    pass
    context = {'kiosk_list': kiosk_list, 'title': title, 'order': order}
    return render_to_response('mapshop/kiosk_list.html', context, RequestContext(request))


def finish_order(request,order_id):
    u''' 
        Заключительная фаза заказа с формой данных о клиенте
    '''
    order= get_object_or_404(Order,id=order_id)
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            order.status = u'Ожидает оплаты'
            order.session = 'done'
            order.save()
            return HttpResponseRedirect('/thanks/')
    else:
        if request.user.is_authenticated():
            client = get_client_or_create(request.user)
            form = ClientForm(instance=client)
        else:
            form = ClientForm()

    context = {'o': order, 'form': form}
    return render_to_response('mapshop/finish_order.html', context, RequestContext(request))


def thanks(request):
    u''' 
        Страница благодарности
    '''
    context = {}
    return render_to_response('mapshop/thanks.html', context, RequestContext(request))



