from django.contrib.auth.models import User
from mapshop.models import Category, Product, ProductImages, Kiosk , Order, Client, Preorder

def create_user(username):
    u = User()
    u.username = username
    u.password = '123'
    u.save()
    c = Client()
    c.user_id = u.id
    c.name = username
    c.email = '%s@mail.ru' % username
    c.save()
    print 'User %s just has been created!' % username
    return c

def create_preloader(client,product):
    p = Preorder.objects.create(contact=client.email, product=product)
    p = Preorder.objects.create(contact='3456789%s' % client.id, product=product, type='phone')
    print 'Preorder (user: %s product: %s) just has been created!' % (client, product)

    
