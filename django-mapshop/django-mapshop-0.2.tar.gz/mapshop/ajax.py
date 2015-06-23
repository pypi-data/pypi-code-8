# -*- coding: utf-8 -*-
from django_ajax.decorators import ajax
from django.shortcuts import render
from mapshop.models import Category, Product, Kiosk, Order, OrderItem, get_client_or_create, Preorder, Client


def get_cart_html(user):
    out = u'<h3> История заказов </h3>'
    out = out + u'<table class="mapshop_cart_table"><tr> <th>Дата</th> <th>Перечень товаров</th> <th>Общая стоимость</th> <th>Статус</th> </tr>'
    client = Client.objects.get(user_id=user.id)
    orders = Order.objects.filter(client=client)
    for o in orders:
        items = '<ul class="mapshop_items">'
        for p in o.orderitem_set.all():
            items = items + '<li>%s</li>' % p.product.name
        items = items + '</ul>'
        out = out + u'<tr><td>%s</td> <td>%s</td> <td>%s руб.</td> <td>%s</td> </tr>' % (o.created_at.strftime('%d.%m.%Y'), items, o.total, o.status,)
    out = out + u'</table>'
    return out

@ajax
def cart_show(request):
    '''  Отображение истории заказов '''
    data = {
            'inner-fragments': { '#mapshop_cart': get_cart_html(request.user)},       
           } 
    return data 

@ajax
def preorder_save(request):
    '''  Cохранение заявки на уведомление о появлении товара '''
    data = {}
    phone = request.GET.get('phone','0')
    email = request.GET.get('email','0')
    product = Product.objects.get(pk=request.GET.get('product_id','0'))
    if phone:
        try:
            p = Preorder.objects.create(contact=phone,product=product,type='phone')
            data = { 'append-fragments': {'#message': '<p>Заявка сохранена!</p>'}}
        except:
            data = {
                    'inner-fragments': { '#error': 'Заявка с такими даннымиы уже существует!'},       
                   }               
    if email:
        try:
            p = Preorder.objects.create(contact=email,product=product,type='email')
            data = { 'append-fragments': {'#message': '<p>Заявка сохранена!</p>'}}
        except:
            data = {
                    'inner-fragments': { '#error': 'Заявка с такими данными уже существует!'},       
                   }     
    return data 
    #try:
    #    p = Preorder.objects.create(pk=request.GET['item_id'])
    #except:
    #    pass

@ajax
def del_product_from_cart(request):
    '''  Удаление товара из корзины и вывод содержимого корзины в html блок <table id="my_busket"></table> '''
    try:
        o = OrderItem.objects.get(pk=request.GET['item_id'])
        o.delete()
    except:
        pass
    session = request.session.session_key
    data = {
            'inner-fragments': { '#my_basket': get_basket_html_by_session_key(session) },       
           }     
    return data

@ajax
def add_product_to_cart(request):
    '''  Добавление товара в корзину и вывод содержимого корзины в html блок <table id="my_busket"></table> '''
    session = request.session.session_key
    #import pdb; pdb.set_trace()
    try:
        product  = Product.objects.get(pk=request.GET.get('product_id',0))
        try:
            order = Order.objects.get(session=session)
        except:
            order = Order()
            order.session = session
            if request.user.is_authenticated():
                client = get_client_or_create(request.user)
                order.client = client
            order.save()
        try:
            item = OrderItem.objects.get(order=order, product=product)
            item.ammount = item.ammount+1
            item.save()
        except:
            item = OrderItem()
            item.product = product
            item.order = order
            item.save()
    except:
        product = None
    data = {
            'inner-fragments': { '#my_basket': get_basket_html_by_session_key(session) },       
           }     
    return data


def get_basket_html_by_session_key(session):
    '''  Получение html кода корзины по идентификатору сессии '''
    from settings import MIN_SUMM
    out = ''
    total = 0
    #import pdb; pdb.set_trace()
    try:
        order = Order.objects.get(session=session)
        if order.orderitem_set.all().count() == 0:
            return u'<b> корзина пуста </b>'
        out = u'<table class="mapshop_basket"><tr><th>Название</th><th>кол-во</th><th>цена</th><th></th></tr>'
        for i in order.orderitem_set.all():
            total = total + (i.ammount*i.product.price)
            out = out + u'<tr><td>%s</td><td>%s</td><td>%s руб.</td><td><a href="#" onclick="return false" data-id=%s class="del_product_from_cart" >X</td></tr>' % (i.product, i.ammount, i.product.price, i.id) 
        out = out + u'<tr><td colspan=3>Итого:</td><td>%s</td></tr>' % total
        out = out + u'</table>'
        if total<MIN_SUMM:
            out = out + u'<span style="color: red"> минимальная стоимость заказа %s </span>' % MIN_SUMM    
        else:
            out = out + u'<a href="/kiosk/list/%s.html">Оформить заказ</a>' % order.id
    except:
        out = u'<b> корзина пуста </b>'
    return out





@ajax
def getinfo_kiosk(request):
    print '----------------------------------%s' % request.GET['kiosk_id']
    ''' выбор киоска  '''
    out = ''
    #try:
    kiosk = Kiosk.objects.get(pk=request.GET['kiosk_id'])
    order = Order.objects.get(pk=request.GET['order_id'])
    if request.user.is_authenticated():
        client = Client.objects.get(user_id=request.user.id)
        client.kiosk = kiosk
        client.save()
    order.kiosk = kiosk
    order.status = u'Киоск выбран'
    order.save()
    context = {'kiosk_name' : kiosk.name,
               'kiosk_address' : kiosk.address,
               'kiosk_scheduler' : kiosk.scheduler,
               'order_id' : request.GET['order_id'],
               'kiosk_foto' : kiosk.foto,
              }
    out = render(request, 'kiosk.html', context)
    #except:
    #    out = 'object does not found'
  
    data = {
            'inner-fragments': { '#kiosk_info': out }
           }
    return data

'''

        <script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax.min.js' %}"></script>
        <script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax-plugin.min.js' %}"></script>

        <script type="text/javascript" src="{% static 'mapsho/static/driver.js' %}"></script>
    



        //// Close private chat **************************
         $('#content').on('click', function(e) {
          
            e.preventDefault();
            
                 ajaxGet('{% url 'ajax-close-private-chat' %}', { 'room_id': room_id }, function(content){ alert(content.myvar) });     
                ajaxGet('/myurl', { 'room_id': room_id }, function(content){});         
            
        });   
        //**************************************************




'''
